import { injury_to_broad_injury } from "./pure"

export interface Fatality {
    name: string;
    date_of_event: string;
    age: number;
    citizenship: string;
    event_location: string;
    event_location_district: string;
    event_location_region: string;
    date_of_death: string;
    gender: string;
    took_part_in_the_hostilities?: any;
    place_of_residence: string;
    place_of_residence_district: string;
    type_of_injury: string;
    broad_injury: ReturnType<typeof injury_to_broad_injury>
    ammunition: string;
    killed_by: string;
    notes: string;
    parsed_date: Date;
    parsed_date_ms: number;
    parsed_date_ms_with_noise: number;
    age_with_noise: number;
    random: number;
}