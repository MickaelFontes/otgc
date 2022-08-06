import re
from datetime import datetime
from sysconfig import is_python_build

from gcsa.event import Event

class EventICS:
    '''Class used to manage the events read from a ICS file.'''
    def __init__(self,
                 t_begin="",
                 t_end="",
                 uid="",
                 sequence="",
                 location="",
                 summary="",
                 description=""):
        self.t_begin = t_begin
        self.t_end = t_end
        self.uid = uid
        self.sequence = sequence
        self.location = location
        self.summary = summary
        self.description = description

    def __str__(self):
        return self.t_begin + '\n' + self.t_end + '\n' + self.uid + '\n' + self.sequence \
            + '\n' + self.location + '\n' + self.summary + '\n' + self.description

    def __eq__(self, other):
        if isinstance(other, EventICS):
            return self.uid == other.uid

    def to_list(self):
        return (self.t_begin, self.t_end, self.location, self.summary,\
                self.description)

    def to_gcsa_event(self):
        '''Return the event as a gcsa event object.'''
        start = datetime.strptime(self.t_begin, '20%y%m%dT%H%M%S')
        end = datetime.strptime(self.t_end, '20%y%m%dT%H%M%S')
        event = Event(summary=self.summary,
                      start=start,
                      end=end,
                      location=self.location,
                      description=self.description,
                      iCalUID=self.uid,
                      sequence=self.sequence)
        return event


class ReaderICS:
    '''Reader used to extract a list of events from a ICS file.'''
    SEPARATORS = ["BEGIN:VEVENT", "END:VEVENT"]
    sep = re.compile('|'.join(SEPARATORS))

    SEPARATORS_FIELDS = [
        "\nDTSTART:", "\nDTEND:", "\nDTSTAMP:", "\nUID:", "\nSEQUENCE:",
        "\nLOCATION:", "\nSUMMARY:", "\nDESCRIPTION:"
    ]
    sep_fields = re.compile('|'.join(SEPARATORS_FIELDS))

    def __init__(self, calendar, is_path=False):
        self.calendar = calendar
        self.is_path = is_path

    def __str__(self):
        return 'ReaderICS used for a ICS'

    def read(self):
        '''Extract a list of EventICS from the ICS provided.'''
        if (self.is_path):
            with open(self.calendar, 'r') as file:
                ics_text = file.read()
        else:
            ics_text = self.calendar
        ics_text = ReaderICS.sep.split(ics_text)
        ics_text = [
            ReaderICS.sep_fields.split(text)[1:] for text in ics_text
            if text.startswith("\nDTSTART:")
        ]
        ics_events = [
            EventICS(t_begin=text[0],
                     t_end=text[1],
                     uid=text[3],
                     sequence=text[4],
                     location=text[5][:-2],
                     summary=text[6][:-3],
                     description=text[7][2:].replace(r'\n', '')) if len(text)
            == 8 else EventICS(t_begin=text[0],
                               t_end=text[1],
                               uid=text[3],
                               sequence=text[4],
                               summary=text[5][:-3],
                               description=text[6][2:].replace(r'\n', ''))
            for text in ics_text
        ]

        return ics_events


if __name__ == "__main__":
    x = ReaderICS('./Downloads/planning.ics')
    events = x.read()
    for ev in events:
        print(ev)
