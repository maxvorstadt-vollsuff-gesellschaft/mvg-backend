from queue import Queue
from threading import Thread
from .models import KickerMatch, Member
from .database import get_db
from sqlalchemy.exc import OperationalError
import time


job_queue = Queue()


def calculate_elo(rating_a, rating_b, score_a, score_b, K=32):
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    expected_b = 1 - expected_a

    outcome_a = 1 if score_a > score_b else 0.5 if score_a == score_b else 0
    outcome_b = 1 - outcome_a

    new_rating_a = rating_a + K * (outcome_a - expected_a)
    new_rating_b = rating_b + K * (outcome_b - expected_b)

    return new_rating_a, new_rating_b


def record_match(match_data, retry_attempts=3, retry_delay=1):
    db = next(get_db())
    attempt = 0

    while attempt < retry_attempts:
        try:
            with db.begin():
                match = KickerMatch(**match_data)

                team_a_player_1: Member | None = db.query(Member).filter(Member.user_sub == match.team_a_player_1).first()
                team_a_player_2: Member | None = db.query(Member).filter(Member.user_sub == match.team_a_player_2).first()
                team_b_player_1: Member | None = db.query(Member).filter(Member.user_sub == match.team_b_player_1).first()
                team_b_player_2: Member | None = db.query(Member).filter(Member.user_sub == match.team_b_player_2).first()

                if not all([team_a_player_1, team_b_player_1]):
                    raise ValueError("One or more players not found")

                rating_a = (team_a_player_1.tkt_elo_rating + (team_a_player_2.tkt_elo_rating if team_a_player_2 else team_a_player_1.tkt_elo_rating)) / 2
                rating_b = (team_b_player_1.tkt_elo_rating + (team_b_player_2.tkt_elo_rating if team_b_player_2 else team_b_player_1.tkt_elo_rating)) / 2

                new_rating_a, new_rating_b = calculate_elo(rating_a, rating_b, match.team_a_score, match.team_b_score)

                team_a_player_1.tkt_elo_rating += (new_rating_a - rating_a) / 2
                if team_a_player_2:
                    team_a_player_2.tkt_elo_rating += (new_rating_a - rating_a) / 2
                team_b_player_1.tkt_elo_rating += (new_rating_b - rating_b) / 2
                if team_b_player_2:
                    team_b_player_2.tkt_elo_rating += (new_rating_b - rating_b) / 2

                db.add(match)

            return

        except OperationalError as e:
            attempt += 1
            if attempt < retry_attempts:
                print(f"Retrying transaction (attempt {attempt}/{retry_attempts}) due to error: {e}")
                time.sleep(retry_delay)
            else:
                print(f"Transaction failed after {retry_attempts} attempts")
                raise e

        except Exception as e:
            db.rollback()
            print(f"Error recording match: {e}")
            break


def process_matches():
    while True:
        match_data = job_queue.get()
        record_match(match_data)
        job_queue.task_done()


def start_elo_processing():
    return Thread(target=process_matches, daemon=True).start()
