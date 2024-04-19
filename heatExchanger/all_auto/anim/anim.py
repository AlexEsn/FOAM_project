import imageio
import os


def create_video_from_images(image_folder, output_video, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(
        ".png") and img.startswith("U")]
    images = sorted(images, key=lambda x: int(
        x.split('U')[1].split('.')[0]))
    print(images)
    image_files = [os.path.join(image_folder, img) for img in images]

    with imageio.get_writer(output_video, fps=fps) as writer:
        for image_file in image_files:
            writer.append_data(imageio.imread(image_file))


# Укажите путь к папке с изображениями
image_folder_path = "./anim/sc"
# Укажите имя и путь к выходному видео
output_video_path = "./anim/video/video2.mp4"
# Укажите количество кадров в секунду
fps = 30

create_video_from_images(image_folder_path, output_video_path, fps)
