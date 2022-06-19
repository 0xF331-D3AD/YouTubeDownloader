import moviepy.editor as mpe


class Combiner:

    @staticmethod
    def combine_video_and_audio(video_name: str, audio_name: str, combined_name: str):
        my_clip = mpe.VideoFileClip(video_name)
        audio_background = mpe.AudioFileClip(audio_name)
        final_clip = my_clip.set_audio(audio_background)
        final_clip.write_videofile(combined_name)
