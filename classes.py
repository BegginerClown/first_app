from transformers import BarkModel, AutoProcessor
import torch
import scipy


def text_to_audio(bark_model='suno/bark', voice_preset='v2/ru_speaker_8'):
    model = BarkModel.from_pretrained(bark_model)
    print('Инициализация прошла')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Инициализация девайса: {device}')
    model = model.to(device)
    processor = AutoProcessor.from_pretrained(bark_model)
    print('processor init')

    text = 'Закончилась батарейка'
    inputs = processor(text, voice_preset=voice_preset).to(device)
    print('start')
    audio_array = model.generate(**inputs)
    print('going')
    audio_array = audio_array.cpu().numpy().squeeze()
    print('audio go')

    sample_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write(f'{voice_preset.split("/")[1]}.wav', rate=sample_rate,data=audio_array)
    print('done')

def main():
    text_to_audio()


if __name__ == '__main__':
    main()

#https://www.youtube.com/watch?v=R59bwGBMn7s&t=522s
#https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c
#https://github.com/suno-ai/bark?tab=readme-ov-file
#https://www.youtube.com/watch?v=UgHWlE7gQHI
