/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { mapValues } from '../runtime';
import type { Member } from './Member';
import {
    MemberFromJSON,
    MemberFromJSONTyped,
    MemberToJSON,
    MemberToJSONTyped,
} from './Member';

/**
 * 
 * @export
 * @interface Event
 */
export interface Event {
    /**
     * 
     * @type {string}
     * @memberof Event
     */
    name: string;
    /**
     * 
     * @type {Date}
     * @memberof Event
     */
    startTime: Date;
    /**
     * 
     * @type {string}
     * @memberof Event
     */
    location: string | null;
    /**
     * 
     * @type {number}
     * @memberof Event
     */
    duration?: number | null;
    /**
     * 
     * @type {number}
     * @memberof Event
     */
    id: number;
    /**
     * 
     * @type {Array<Member>}
     * @memberof Event
     */
    participants: Array<Member>;
    /**
     * 
     * @type {Member}
     * @memberof Event
     */
    author: Member | null;
}

/**
 * Check if a given object implements the Event interface.
 */
export function instanceOfEvent(value: object): value is Event {
    if (!('name' in value) || value['name'] === undefined) return false;
    if (!('startTime' in value) || value['startTime'] === undefined) return false;
    if (!('location' in value) || value['location'] === undefined) return false;
    if (!('id' in value) || value['id'] === undefined) return false;
    if (!('participants' in value) || value['participants'] === undefined) return false;
    if (!('author' in value) || value['author'] === undefined) return false;
    return true;
}

export function EventFromJSON(json: any): Event {
    return EventFromJSONTyped(json, false);
}

export function EventFromJSONTyped(json: any, ignoreDiscriminator: boolean): Event {
    if (json == null) {
        return json;
    }
    return {
        
        'name': json['name'],
        'startTime': (new Date(json['start_time'])),
        'location': json['location'],
        'duration': json['duration'] == null ? undefined : json['duration'],
        'id': json['id'],
        'participants': ((json['participants'] as Array<any>).map(MemberFromJSON)),
        'author': MemberFromJSON(json['author']),
    };
}

  export function EventToJSON(json: any): Event {
      return EventToJSONTyped(json, false);
  }

  export function EventToJSONTyped(value?: Event | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'name': value['name'],
        'start_time': ((value['startTime']).toISOString()),
        'location': value['location'],
        'duration': value['duration'],
        'id': value['id'],
        'participants': ((value['participants'] as Array<any>).map(MemberToJSON)),
        'author': MemberToJSON(value['author']),
    };
}
