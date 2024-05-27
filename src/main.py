from distro250ls import encode, decode
import subprocess, argparse, contextlib
from pathlib import Path

currentWorkingDir = Path.cwd()
parentDir = currentWorkingDir.parent
requirementsLocation = parentDir / "requirements.txt"

try:
    from PIL import Image
    import gradio as gr
    import ast, io, base64, qrcode, webbrowser
except:
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip", "--user"])
    subprocess.run(["pip", "install", "-r", str(requirementsLocation), "--user"])
    print("!!!ALL PACKAGES ARE DOWNLOADED, PLEASE RUN PROGRAM AGAIN!!!")
    exit()


def encodeUI(chipertext: str):
    return encode(chipertext)


def decodeUI(encodedText: str):
    encodedList = ast.literal_eval(encodedText)
    return decode(encodedList)


def encodeImage(image: Image.Image, width=300, height=300):
    image.thumbnail((width, height), Image.Resampling.LANCZOS)
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    return encode(encoded_image)


def decodeImage(encodedImageText: str):
    encodedImageList = ast.literal_eval(encodedImageText)
    decodedImageText = decode(encodedImageList)
    decoded_image_data = base64.b64decode(decodedImageText)
    image = Image.open(io.BytesIO(decoded_image_data))
    return image


def generateQRcode(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = "qr_code.png"
    img.save(img_path)
    return img_path


def encFile(file):
    with open(file, "r") as f:
        content = f.read()
    return encode(content)


def encAudio(fileP):
    with open(fileP, "rb") as f:
        contents = f.read()

    return encode(str(contents))


def decAudio(encAudioText):
    encAudioList = ast.literal_eval(encAudioText)
    decAudioText = decode(encAudioList)
    return decAudioText


def encVideo(video):
    with open(video, "rb") as f:
        contents = f.read()

    return encode(str(contents))


def decVideo(encVideoText):
    encVideoList = ast.literal_eval(encVideoText)
    decAudioText = decode(encVideoList)
    return decAudioText


margin = """<div style="margin-top: 150px;"></div>"""
callback = gr.CSVLogger()

with gr.Blocks(title="Distro25o") as demo:
    inputEnc = gr.Textbox(label="Chipertext")
    outputEnc = gr.Textbox(label="Encoded Text")
    encodeButton = gr.Button("Encode Text")
    encodeButton.click(encodeUI, inputs=inputEnc, outputs=outputEnc)

    gr.Markdown(margin)

    inputDec = gr.Textbox(label="Encoded Text")
    outputDec = gr.Textbox(label="Chipertext")
    decodeButton = gr.Button("Decode Text")
    decodeButton.click(decodeUI, inputs=inputDec, outputs=outputDec)

    gr.Markdown(margin)

    inputFileEnc = gr.UploadButton(label="Upload File", type="filepath")
    outputFileEnc = gr.Textbox(label="Encoded File")
    fileEncButton = gr.Button("Encode File")
    fileEncButton.click(fn=encFile, inputs=inputFileEnc, outputs=outputFileEnc)

    gr.Markdown(margin)

    audioInputEnc = gr.Audio(label="Upload Audio", type="filepath")
    audioOutputEnc = gr.Textbox(label="Encoded File")
    audioEncButton = gr.Button("Encode Audio")
    audioEncButton.click(fn=encAudio, inputs=audioInputEnc, outputs=audioOutputEnc)

    gr.Markdown(margin)

    audioInputDec = gr.Textbox(label="Encoded Audio")
    audioOutputDec = gr.Audio(label="Decoded Audio")
    audioDecButton = gr.Button("Decode Audio")
    audioDecButton.click(fn=decAudio, inputs=audioInputDec, outputs=audioOutputDec)

    gr.Markdown(margin)

    imageSizeW = gr.Number(label="Image Width")
    imageSizeH = gr.Number(label="Image Height")

    imgInputEnc = gr.Image(type="pil", label="Input Image")
    imgOutputEnc = gr.Textbox(label="Encoded Image")
    imgEncodeButton = gr.Button("Encode Image")
    imgEncodeButton.click(
        encodeImage, inputs=[imgInputEnc, imageSizeW, imageSizeH], outputs=imgOutputEnc
    )

    gr.Markdown(margin)

    imgInputDec = gr.Textbox(label="Encoded Image")
    imgOutputDec = gr.Image(type="pil", label="Decoded Image")
    imgEncodeButton = gr.Button("Decode Image")
    imgEncodeButton.click(decodeImage, inputs=imgInputDec, outputs=imgOutputDec)

    gr.Markdown(margin)

    videoInputEnc = gr.Video(label="Input Video")
    videoOutputEnc = gr.Textbox(label="Encoded Video")
    videoEncodeButton = gr.Button("Encode Video")
    videoEncodeButton.click(encVideo, inputs=videoInputEnc, outputs=videoOutputEnc)

    gr.Markdown(margin)

    videoInputDec = gr.Textbox(label="Encoded Video")
    videoOutputDec = gr.Video(label="Decoded Video")
    videoDecodeButton = gr.Button("Decode Video")
    videoDecodeButton.click(decVideo, inputs=videoInputDec, outputs=videoOutputDec)

    btnSaveData = gr.Button("Save Data")

    callback.setup(
        [
            inputEnc,
            outputEnc,
            inputDec,
            outputDec,
            imageSizeW,
            imageSizeH,
            imgInputEnc,
            imgOutputEnc,
            imgInputDec,
            imgOutputDec,
        ],
        "flagged_data_points",
    )
    btnSaveData.click(
        lambda *args: callback.flag(args),
        [
            inputEnc,
            outputEnc,
            inputDec,
            outputDec,
            imageSizeW,
            imageSizeH,
            imgInputEnc,
            imgOutputEnc,
            imgInputDec,
            imgOutputDec,
        ],
        None,
        preprocess=False,
    )

    # QRLink = "https://github.com/Hipex123"
    # qrImage = gr.Image(generateQRcode(QRLink))

    gr.Markdown(
        """
            <div style="text-align: right; margin-top: 20px;">
                <a href="https://github.com/Hipex123" target="_blank" style="font-size: 25px; color: white;">
                    View on GitHub
                </a>
            </div>
        """
    )

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--share",
    action="store_true",
    help="share your web server with a public domain (must be used with -r flag)",
)
parser.add_argument(
    "-r",
    "--run",
    action="store_true",
    help="start a web server",
)

args = parser.parse_args()
buffer = io.StringIO()

if args.run and args.share:
    with contextlib.redirect_stdout(buffer):
        demo.launch(share=True, prevent_thread_lock=True)

    output = buffer.getvalue()
    print(output)
    for line in output.splitlines():
        if "Running on public URL:" in line:
            publicUrl = line[23:]

    webbrowser.open(publicUrl)

elif args.run and not args.share:
    demo.launch(prevent_thread_lock=True)
    webbrowser.open("http://127.0.0.1:7860/")
elif args.share and not args.run:
    print("No run flag specified.")
    print("Quitting...")


input("Press key to shutdown server...")
