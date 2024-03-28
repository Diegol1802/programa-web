import os
import moviepy.editor as mp
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class VideoEditor:
    def __init__(self):
        self.video_path = None
        self.image_path = None
        self.audio_path = None
        self.second_image_path = None

    def overlay_image(self):
        if self.video_path and self.image_path and self.audio_path and self.second_image_path:
            try:
                video = mp.VideoFileClip(self.video_path)
                # Get dimensions of the first image
                image1 = mp.ImageClip(self.image_path)
                image_width, image_height = image1.size
                
                # Check if image dimensions are different from video dimensions
                if image_width != video.size[0] or image_height != video.size[1]:
                    # Resize the video to match image dimensions
                    video = video.resize((image_width, image_height))       

                audio = mp.AudioFileClip(self.audio_path2)

                # Load original audio of the video
                original_audio = audio

                # Load background audio track
                background_audio = mp.AudioFileClip(self.audio_path)

                # Adjust volume of the background audio
                background_audio = background_audio.volumex(0.20)  # Adjust volume to 20% of the original volume

                # Calculate the total duration of video
                total_duration = video.duration

                # Overlay the first image onto the video
                overlay_image_clip1 = image1.set_duration(total_duration)  # Duration matches the video duration
                final_clip = mp.CompositeVideoClip([video, overlay_image_clip1])

                # Add the second PNG image after the video
                image2 = mp.ImageClip(self.second_image_path)
                overlay_image_clip2 = image2.set_duration(6)  # Assuming second image has a duration of 6 seconds
                final_clip = mp.concatenate_videoclips([final_clip, overlay_image_clip2])

                # Calculate remaining duration after the second image
                remaining_duration = total_duration + overlay_image_clip2.duration

                # Adjust background audio duration to match total duration
                background_audio = background_audio.set_duration(remaining_duration)

                # Fade out the background audio 2 seconds before the end
                background_audio = background_audio.audio_fadeout(2)

                # Overlay the background audio on the original audio
                final_audio = mp.CompositeAudioClip([original_audio, background_audio])

                 # Set the composite audio track to the video
                final_clip = final_clip.set_audio(final_audio)


                output_folder = r"C:\programa por web\Menu Video Editor\uploads"
                output_filename = "output.mp4"
                output_path = os.path.join("static", output_folder, output_filename)
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", audio_bitrate="320k", bitrate="10000k", fps=30)
                return output_path
            except Exception as e:
                return str(e)
        else:
            return "Por favor, seleccione un Video, una imagen PNG, una Segunda imagen PNG y una Música de Fondo."

video_editor = VideoEditor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files['video']
        audio_file2 = request.files['audio2']
        image_file = request.files['image']
        audio_file = request.files['audio']
        second_image_file = request.files['second_image']
        
        video_path = os.path.join('uploads', video_file.filename)
        audio_path2 = os.path.join('uploads', audio_file2.filename)
        image_path = os.path.join('uploads', image_file.filename)
        audio_path = os.path.join('uploads', audio_file.filename)
        second_image_path = os.path.join('uploads', second_image_file.filename)
        
        video_file.save(video_path)
        audio_file2.save(audio_path2)
        image_file.save(image_path)
        audio_file.save(audio_path)
        second_image_file.save(second_image_path)
        
        video_editor.video_path = video_path
        video_editor.audio_path2 = audio_path2
        video_editor.image_path = image_path
        video_editor.audio_path = audio_path
        video_editor.second_image_path = second_image_path
        
        output_path = video_editor.overlay_image()
        if output_path:
            return redirect(url_for('result', filename=os.path.basename(output_path)))
        else:
            return "Hubo un error al procesar el video."
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
        app.run(host='servidor', port=6001, debug=True)
