import magenta
import note_seq
import tensorflow
from note_seq.protobuf import music_pb2
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2
from note_seq import midi_io

#sample sequences

drums = music_pb2.NoteSequence()

drums.notes.add(pitch=36, start_time=0, end_time=0.125, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=38, start_time=0, end_time=0.125, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=42, start_time=0, end_time=0.125, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=46, start_time=0, end_time=0.125, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=42, start_time=0.25, end_time=0.375, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=42, start_time=0.375, end_time=0.5, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=42, start_time=0.5, end_time=0.625, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=50, start_time=0.5, end_time=0.625, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=36, start_time=0.75, end_time=0.875, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=38, start_time=0.75, end_time=0.875, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=42, start_time=0.75, end_time=0.875, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=45, start_time=0.75, end_time=0.875, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=36, start_time=1, end_time=1.125, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=42, start_time=1, end_time=1.125, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=46, start_time=1, end_time=1.125, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=42, start_time=1.25, end_time=1.375, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=48, start_time=1.25, end_time=1.375, is_drum=True, instrument=10, velocity=80)
drums.notes.add(pitch=50, start_time=1.25, end_time=1.375, is_drum=True, instrument=10, velocity=80)
drums.total_time = 1.375

drums.tempos.add(qpm=60)



# Initialize the model.
def generateMelody():
  bundle = sequence_generator_bundle.read_bundle_file('./Models/attention_rnn.mag')
  generator_map = melody_rnn_sequence_generator.get_generator_map()
  melody_rnn = generator_map['attention_rnn'](checkpoint=None, bundle=bundle)
  melody_rnn.initialize()


  inputmidi = midi_io.midi_file_to_note_sequence('./Queries/convertMelody.mid')

  input_sequence = inputmidi # change this to teapot if you want
  num_steps = 64 # change this for shorter or longer sequences
  temperature = 1.0 # the higher the temperature the more random the sequence.

  # Set the start time to begin on the next step after the last note ends.
  last_end_time = (max(n.end_time for n in input_sequence.notes)
                    if input_sequence.notes else 0)
  qpm = input_sequence.tempos[0].qpm 
  seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
  total_seconds = num_steps * seconds_per_step

  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = temperature
  generate_section = generator_options.generate_sections.add(
    start_time=last_end_time + seconds_per_step,
    end_time=total_seconds)

  # Ask the model to continue the sequence.
  sequence = melody_rnn.generate(input_sequence, generator_options)

  note_seq.sequence_proto_to_midi_file(sequence, 'melody.mid')


def generateDrums():
  bundle = sequence_generator_bundle.read_bundle_file('./Models/drum_kit_rnn.mag')
  generator_map = drums_rnn_sequence_generator.get_generator_map()
  drums_rnn = generator_map['drum_kit'](checkpoint=None, bundle=bundle)
  drums_rnn.initialize()

  inputmidi = midi_io.midi_file_to_note_sequence('./Queries/convertDrum.mid')

  input_sequence = inputmidi # change this to teapot if you want
  num_steps = 64 # change this for shorter or longer sequences
  temperature = 1.0 # the higher the temperature the more random the sequence.

  # Set the start time to begin on the next step after the last note ends.
  last_end_time = (max(n.end_time for n in input_sequence.notes)
                    if input_sequence.notes else 0)
  qpm = input_sequence.tempos[0].qpm 
  seconds_per_step = 60.0 / qpm / drums_rnn.steps_per_quarter
  total_seconds = num_steps * seconds_per_step

  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = temperature
  generate_section = generator_options.generate_sections.add(
    start_time=last_end_time + seconds_per_step,
    end_time=total_seconds)

  # Ask the model to continue the sequence.
  sequence = drums_rnn.generate(input_sequence, generator_options)

  note_seq.sequence_proto_to_midi_file(sequence, 'drums.mid')

generateMelody()