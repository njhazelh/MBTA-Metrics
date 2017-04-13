export const LINES = {
  Fairmount: 'CR-Fairmount',
  Fitchburg: 'CR-Fitchburg',
  Franklin: 'CR-Franklin',
  Greenbush: 'CR-Greenbush',
  Haverhill: 'CR-Haverhill',
  'Kingston/Plymouth': 'CR-Kingston',
  Lowell: 'CR-Lowell',
  'Middleborough/Lakeville': 'CR-Middleborough',
  Needham: 'CR-Needham',
  'Newbury/Rockport': 'CR-Newburyport',
  'Providence/Stoughton': 'CR-Providence',
  'Framingham/Worcester': 'CR-Worcester',
};

export const LINE_KEYS = Object.keys(LINES);
export const LINE_VALUES = Object.values(LINES);

export const ALERTS = [
  'Existent', 'Nonexistent',
  'Timely', 'Late',
  'Accurate', 'Inaccurate',
];

export const DIRECTIONS = ['Inbound', 'Outbound'];

export const FROM_DATE = 'fromDate';
export const TO_DATE = 'toDate';
export const FROM_TIME = 'fromTime';
export const TO_TIME = 'toTime';
