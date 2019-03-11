import os
import sys
import h5py
import re
# path to settings
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
from settings import REAL_DATA_PREDICTIONS, SHEETS_DIR, ABJAD_TONES, BEAT
from abjad import Staff, Voice, LilyPondLiteral, attach, Container, show
from abjad.system.PersistenceManager import PersistenceManager


class ToneParser:

    tone_list = []

    def __init__(self, filename):
        file = h5py.File(os.path.join(REAL_DATA_PREDICTIONS, filename), 'r')
        self.tone_list = file['predictions'].value
        file.close()
        self.strip_silence()

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

    def get_abjad_tones(self, tone_class_name):
        '''
        Returns tuple containing mala and vela values.
        '''

        try:
            mala = re.search('m\d', tone_class_name).group(0)
        except AttributeError:
            mala = None

        try:
            vela = re.search('v\d', tone_class_name).group(0)
        except AttributeError:
            vela = None

        # pause
        if not mala:
            mala = 'pause'
        if not vela:
            vela = 'pause'

        return (ABJAD_TONES[mala], ABJAD_TONES[vela])

    def merge_same_tones(self, tone_list):
        '''
        tone_list => list of tuples containing information about mala class,
        vela class and duration.
        Returns squashed list with distinct values in sequence array example:
        aaabbbccc becomes abc
        '''
        merged_tone_list = {'m': [], 'v': []}

        prev_mala = tone_list[0][0]
        prev_vela = tone_list[0][1]

        # same length on the beggining
        prev_mala_tone_length = tone_list[0][2]
        prev_vela_tone_length = tone_list[0][2]

        for mala_tone, vela_tone, tone_length in tone_list[1:]:

            if prev_mala == mala_tone:
                prev_mala_tone_length += tone_length
            else:
                merged_tone_list['m'].append((prev_mala, prev_mala_tone_length))
                prev_mala_tone_length = tone_length
                prev_mala = mala_tone

            if prev_vela == vela_tone:
                prev_vela_tone_length += tone_length
            else:
                merged_tone_list['v'].append((prev_vela, prev_vela_tone_length))
                prev_vela_tone_length = tone_length
                prev_vela = vela_tone

        # append last tone
        if prev_mala_tone_length > 0:
            merged_tone_list['m'].append((prev_mala, prev_mala_tone_length))

        if prev_vela_tone_length > 0:
            merged_tone_list['v'].append((prev_vela, prev_vela_tone_length))

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
                mala_tone, vela_tone = self.get_abjad_tones(prev)

                if tone_length <= IGNORE_THRESHOLD:
                    transition_length += tone_length
                else:
                    tone_list.append(
                        (mala_tone, vela_tone, tone_length + transition_length)
                    )
                    transition_length = 0
                # reset
                tone_length = 0
                prev = tone_class_name

        # append last
        if tone_length >= IGNORE_THRESHOLD:
            last_dict_name = self.tone_list[-1]
            mala_tone, vela_tone = self.get_abjad_tones(last_dict_name)
            tone_list.append((mala_tone, vela_tone, tone_length))

        # tones are here in abjad format (not in class format)
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

        mala_voice = ""
        vela_voice = ""
        tones_dict = self.get_tones_dict()
        for mala_tone, tone_length in tones_dict['m']:
            duration = self.get_duration_label(tone_length)

            if duration:
                mala_voice += mala_tone + duration + " "

        for vela_tone, tone_length in tones_dict['v']:
            duration = self.get_duration_label(tone_length)

            if duration:
                vela_voice += vela_tone + duration + " "

        mala_voice = Voice(mala_voice, name='mala voice')
        literal = LilyPondLiteral(r'\voiceOne')
        attach(literal, mala_voice)

        vela_voice = Voice(vela_voice, name='vela voice')
        literal = LilyPondLiteral(r'\voiceTwo')
        attach(literal, vela_voice)

        container = Container([mala_voice, vela_voice])
        container.is_simultaneous = True
        notes.append(container)

        # show(notes)
        PersistenceManager(client=notes).as_pdf(os.path.join(SHEETS_DIR, filename))


for filename in os.listdir(REAL_DATA_PREDICTIONS):
    print("Filename: %s" % (filename))
    sheet = ToneParser(filename)
    sheet.parse_tones(filename)


# sheet = ToneParser('sadila_je_mare.hdf5')
# sheet.parse_tones('sadila_je_mare')
