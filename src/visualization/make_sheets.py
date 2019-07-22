import os
import sys
import h5py
import re
from abjad.system.PersistenceManager import PersistenceManager
from abjad import Staff, Voice, LilyPondLiteral, attach, Container
# path to settings
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
from settings import REAL_DATA_PREDICTIONS, SHEETS_DIR, \
    ABJAD_TONES, BEAT, CUT_DIR, ML_MODELS


class ToneParser:

    tone_list = []

    def __init__(self, filename, class_labels=None):
        file = h5py.File(os.path.join(REAL_DATA_PREDICTIONS, filename), 'r')
        self.tone_list = file['predictions'].value
        file.close()

        if class_labels:
            # parse number to names
            new_tone_list = []
            for tone in self.tone_list:
                new_tone_list.append(
                    self.index_to_class_name(tone, class_labels)
                )
            self.tone_list = new_tone_list
            self.strip_silence()

    def index_to_class_name(self, index, class_labels):
        """
        index -> integer representing class
        class_labels -> list of folders in a cut dir

        returns string representation of class, depending on
        the folder name in the CUT_DIR
        """
        return class_labels[index]

    def strip_silence(self):
        """
        Returns list without first and last n examples of silence class (13).
        """
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
        """
        Returns tuple containing mala and vela values.
        """

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

    def get_abjad_tone(self, tone_class_name):
        """
        Returns tuple containing mala and vela values.
        """

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

    def merge_same_tones_mono(self, tone_list):
        """
        tone_list => list of tuples containing information about mala class,
        vela class and duration.
        Returns squashed list with distinct values in sequence array example:
        aaabbbccc becomes abc
        """
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

    def merge_same_tones_poly(self, tone_list):
        """
        tone_list => list of tuples containing information about mala class,
        vela class and duration.
        Returns squashed list with distinct values in sequence array example:
        aaabbbccc becomes abc
        """
        merged_tone_list = {'m': [], 'v': []}

        prev_mala = tone_list[0][0]
        prev_vela = tone_list[0][1]

        # same length on the beginning
        prev_mala_tone_length = tone_list[0][2]
        prev_vela_tone_length = tone_list[0][2]

        for mala_tone, vela_tone, tone_length in tone_list[1:]:

            if prev_mala == mala_tone:
                prev_mala_tone_length += tone_length
            else:
                merged_tone_list['m'].append(
                    (prev_mala, prev_mala_tone_length)
                )
                prev_mala_tone_length = tone_length
                prev_mala = mala_tone

            if prev_vela == vela_tone:
                prev_vela_tone_length += tone_length
            else:
                merged_tone_list['v'].append(
                    (prev_vela, prev_vela_tone_length)
                )
                prev_vela_tone_length = tone_length
                prev_vela = vela_tone

        # append last tone
        if prev_mala_tone_length > 0:
            merged_tone_list['m'].append((prev_mala, prev_mala_tone_length))

        if prev_vela_tone_length > 0:
            merged_tone_list['v'].append((prev_vela, prev_vela_tone_length))

        return merged_tone_list

    def get_tones_dict_mono(self):
        """
        Returns tuple containing two list of tuples. First list is set of
        tone and duration values of 'mala' and second are values of 'vela'.
        First value in each tuple is abjad tone name and second value is
        number of consecutive frames with that tone.
        """
        tone_list = []
        tone_length = 0
        # if tone is misclassified then tone length is assigned to next tone
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

        return self.merge_same_tones_mono(tone_list)

    def get_tones_dict_poly(self):
        """
        Returns tuple containing two list of tuples. First list is set of
        tone and duration values of 'mala' and second are values of 'vela'.
        First value in each tuple is abjad tone name and second value is
        number of consecutive frames with that tone.
        """
        tone_list = []
        tone_length = 0
        # if tone is misclassified then tone length is assigned to next tone
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

        return self.merge_same_tones_poly(tone_list)

    @staticmethod
    def get_duration_label(frames):

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

    def parse_tones_poly(self, filename, model_name):
        notes = Staff()
        # remove measure and tacts
        notes.remove_commands.append('Time_signature_engraver')
        notes.remove_commands.append('Bar_engraver')

        mala_voice = ""
        vela_voice = ""
        tones_dict = self.get_tones_dict_poly()
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

        PersistenceManager(client=notes).as_pdf(
            os.path.join(SHEETS_DIR, model_name, filename)
        )

    def parse_tones_mono(self, filename, model_name):
        notes = Staff()
        # remove measure and tacts
        notes.remove_commands.append('Time_signature_engraver')
        notes.remove_commands.append('Bar_engraver')

        for tone, tone_length in self.get_tones_dict():
            duration = self.get_duration_label(tone_length)

            if duration:
                tone += duration

                notes.append(tone)

        PersistenceManager(client=notes).as_pdf(
            os.path.join(SHEETS_DIR, model_name, filename)
        )


for model in ML_MODELS:
    print("Model: %s" % (model['name']))

    class_labels = None
    if model['model_type'] == 'cnn':
        class_labels = os.listdir(os.path.join(CUT_DIR, model['name']))
        class_labels.sort()

    for filename in os.listdir(
            os.path.join(REAL_DATA_PREDICTIONS, model['name'])):
        print("Filename: %s" % filename)
        sheet = ToneParser(filename, model['name'], class_labels)
        if model['voice_type'] == 'mono':
            sheet.parse_tones_mono(filename, model['name'])
        else:
            sheet.parse_tones_poly(filename, model['name'])
