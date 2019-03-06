import os
import sys
import h5py
import re
# path to settings
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
from settings import REAL_DATA_PREDICTIONS, SHEETS_DIR, ABJAD_TONES, BEAT, CUT_DIR
from abjad import Staff
from abjad.system.PersistenceManager import PersistenceManager

class_labels = os.listdir(CUT_DIR)
class_labels.sort()


class ToneParser:

    tone_list = []

    def __init__(self, filename):
        file = h5py.File(os.path.join(REAL_DATA_PREDICTIONS, filename), 'r')
        self.tone_list = file['predictions'].value
        file.close()
        self.strip_silence()

    def index_to_class_name(self, index):
        return class_labels[index]

    def strip_silence(self):
        '''
        Returns list without first and last n examples of silence class (13).
        '''
        start_idx = 0
        end_idx = -1
        # class position
        for i, tone in enumerate(self.tone_list):
            if not 'silence' in tone:
                start_idx = i
                break

        for i, tone in reversed(list(enumerate(self.tone_list))):
            if not 'silence' in tone:
                end_idx = i - 1
                break

        self.tone_list = self.tone_list[start_idx:end_idx]

    def get_abjad_tone(self, tone_class_name):
        '''
        Returns tuple containing mala and vela values.
        '''

        try:
            tone = re.search('m\d', tone_class_name).group(0)
        except AttributeError:
            tone = None

        # if mala does not exist search for vela
        if not tone:
            try:
                tone = re.search('v\d', tone_class_name).group(0)
            except AttributeError:
                tone = None

        # pause
        if not tone:
            tone = 'pause'

        return ABJAD_TONES[tone]

    def merge_same_tones(self, tone_list):
        '''
        tone_list => list of tuples containing information about mala class,
        vela class and duration.
        Returns squashed list with distinct values in sequence array example:
        aaabbbccc becomes abc
        '''
        merged_tone_list = []

        prev = tone_list[0]
        prev_tone_length = prev[1]
        for tone, tone_length in tone_list[1:]:
            if prev[0] == tone:
                prev_tone_length += tone_length
            else:
                merged_tone_list.append((prev[0], prev_tone_length))
                prev_tone_length = tone_length
                prev = (tone, tone_length)
        if prev_tone_length > 0:
            merged_tone_list.append((prev[0], prev_tone_length))
        return merged_tone_list

    def get_tones_dict(self):
        '''
        Returnes tuple containing two list of tuples. First list is set of
        tone and duration values of 'mala' and second are values of 'vela'.
        First value in each tuple is abjad tone name and second value is
        number of consecutive frames with that tone.
        '''
        tone_list = []
        tone_length = 0
        # if tone is missclassified then tone length is assigned to next tone
        transition_length = 0
        IGNORE_THRESHOLD = 3

        prev = self.tone_list[0]
        for i, tone_class_name in enumerate(self.tone_list[1:]):
            tone_length += 1
            if prev != tone_class_name:
                tone = self.get_abjad_tone(prev)

                if tone_length <= IGNORE_THRESHOLD:
                    transition_length += tone_length
                else:
                    tone_list.append(
                        (tone, tone_length + transition_length)
                    )
                    transition_length = 0
                # reset
                tone_length = 0
                prev = tone_class_name

        # append last
        if tone_length >= IGNORE_THRESHOLD:
            last_dict_name = self.tone_list[-1]
            tone = self.get_abjad_tone(last_dict_name)
            tone_list.append((tone, tone_length))

        return self.merge_same_tones(tone_list)

    def get_duration_label(self, frames):

        if frames > 4 * BEAT:
            return '1'
        elif frames > 2 * BEAT:
            return '2'
        elif frames > BEAT:
            return '4'
        elif frames > BEAT / 2:
            return '8'
        elif frames > BEAT / 4:
            return '16'
        # elif frames > BEAT / 8:
        #     return '32'
        # if beat is smaller then it is discarded
        return None

    def parse_tones(self, filename):
        notes = Staff()
        # remove measure and tacts
        notes.remove_commands.append('Time_signature_engraver')
        notes.remove_commands.append('Bar_engraver')

        for tone, tone_length in self.get_tones_dict():
            duration = self.get_duration_label(tone_length)

            if duration:
                tone += duration

                notes.append(tone)

        PersistenceManager(client=notes).as_pdf(os.path.join(SHEETS_DIR, filename))


for filename in os.listdir(REAL_DATA_PREDICTIONS):
    print("Filename: %s" % (filename))
    sheet = ToneParser(filename)
    sheet.parse_tones(filename)


# sheet = ToneParser('sadila_je_mare.hdf5')
# sheet.parse_tones('sadila_je_mare')
