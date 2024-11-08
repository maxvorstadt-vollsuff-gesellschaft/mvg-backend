from enum import Enum

class Roles(str, Enum):
    GUEST = "guest"
    MKM_MEMBER = "mkm-member"
    MVG_MEMBER = "mvg-member"

ROLE_HIERARCHY = {
    Roles.MVG_MEMBER: [Roles.MVG_MEMBER, Roles.MKM_MEMBER, Roles.GUEST],
    Roles.MKM_MEMBER: [Roles.MKM_MEMBER, Roles.GUEST],
    Roles.GUEST: [Roles.GUEST]
}

def check_user_access(user_role: str, required_role: Roles) -> bool:
    # Convert string to enum if needed
    user_role_enum = Roles(user_role)
    
    # Example role hierarchy
    role_hierarchy = {
        Roles.MVG_MEMBER: [Roles.MVG_MEMBER, Roles.MKM_MEMBER, Roles.GUEST],
        Roles.MKM_MEMBER: [Roles.MKM_MEMBER, Roles.GUEST],
        Roles.GUEST: [Roles.GUEST]
    }
    
    return user_role_enum in role_hierarchy[required_role]
