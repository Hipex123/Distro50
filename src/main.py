from libs.distro250ls import encode, decode
import argparse, contextlib, webbrowser, base64, io, ast, msvcrt, qrcode, datetime
from PIL import Image
import gradio as gr

def encodeUI(plaintext: str):
    return encode(plaintext)


def decodeUI(ciphertext: str):
    encodedList = ast.literal_eval(ciphertext)
    return decode(encodedList)


def encodeImage(image: Image.Image, width=300, height=300):
    currDatetime = datetime.datetime.now()

    image.thumbnail((width, height), Image.Resampling.NEAREST)
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

    f = open(f"../saved_files/cipher/images/image-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8")

    f.write(str(encode(encoded_image)))
    f.close()

def decodeImageSave(file):
    currDatetime = datetime.datetime.now()

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    encodedImageList = ast.literal_eval(content)
    decodedImageText = decode(encodedImageList)
    decoded_image_data = base64.b64decode(decodedImageText)
    image = Image.open(io.BytesIO(decoded_image_data))

    image.save(f"../saved_files/plain/images/image-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.png")

def decodeImage(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    encodedImageList = ast.literal_eval(content)
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


def encFile(plainFile):
    currDatetime = datetime.datetime.now()

    with open(plainFile, "r", encoding="utf-8") as f:
        content = f.read()

    f = open(f"../saved_files/cipher/files/file-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8")

    f.write(str(encode(content)))
    f.close()

def decFileSave(cipherFile):
    currDatetime = datetime.datetime.now()

    with open(cipherFile, "r", encoding="utf-8") as f:
        content = f.read()

    f = open(f"../saved_files/plain/files/file-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8")

    f.write(decode(ast.literal_eval(content)))
    f.close()

def decFile(cipherFile):
    with open(cipherFile, "r", encoding="utf-8") as f:
        content = f.read()
    return decode(ast.literal_eval(content))


def encAudio(plainFile):
    currDatetime = datetime.datetime.now()

    with open(plainFile, "rb") as f:
        content = f.read()

    encodedContent = base64.b64encode(content).decode("utf-8")

    f = open(f"../saved_files/cipher/audio/audio-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8")

    f.write(str(encode(encodedContent)))
    f.close()



def decAudio(chiperFile):
    with open(chiperFile, "r", encoding="utf-8") as f:
        contents = ast.literal_eval(f.read())

    decodedContent = decode(contents)
    decodedContentBin = base64.b64decode(decodedContent)

    with open("../saved_files/temps/temp.mp3", "wb") as f:
        f.write(decodedContentBin)
    f.close()

    return "../saved_files/temps/temp.mp3"


def encVideo(plainVideo):
    with open(plainVideo, "rb") as f:
        contents = f.read()

    return encode(str(contents))


def decVideo(cipherVideo):
    encVideoList = ast.literal_eval(cipherVideo)
    decAudioText = decode(encVideoList)
    return decAudioText


margin = """<div style="margin-top: 150px;"></div>"""
callback = gr.CSVLogger()

with gr.Blocks(title="Distro50") as demo:
    # TEXT
    inputEnc = gr.Textbox(label="Plaintext")
    outputEnc = gr.Textbox(label="Ciphertext")
    encodeButton = gr.Button("Encode Text")
    encodeButton.click(encodeUI, inputs=inputEnc, outputs=outputEnc)

    gr.Markdown(margin)

    inputDec = gr.Textbox(label="Ciphertext")
    outputDec = gr.Textbox(label="Plaintext")
    decodeButton = gr.Button("Decode Text")
    decodeButton.click(decodeUI, inputs=inputDec, outputs=outputDec)

    gr.Markdown(margin)

    # FILES

    inputFileEnc = gr.UploadButton(label="Upload Plain File", type="filepath")
    fileEncButton = gr.Button("Encode File")
    fileEncButton.click(fn=encFile, inputs=inputFileEnc)

    gr.Markdown(margin)

    inputFileDec = gr.UploadButton(label="Upload Cipher File", type="filepath")
    fileDecButton = gr.Button("Decode File")
    fileDecButtonSave = gr.Button("Save Plain File")
    outputFileDec = gr.Textbox(label="Plain File")
    fileDecButton.click(fn=decFile, inputs=inputFileDec, outputs=outputFileDec)
    fileDecButtonSave.click(fn=decFileSave, inputs=inputFileDec)
    
    gr.Markdown(margin)

    # AUDIO

    audioInputEnc = gr.Audio(label="Upload Plain Audio", type="filepath")
    audioEncButton = gr.Button("Encode Audio")
    audioEncButton.click(fn=encAudio, inputs=audioInputEnc)

    gr.Markdown(margin)

    audioInputDec = gr.UploadButton(label="Upload Cipher Audio", type="filepath")
    audioOutputDec = gr.Audio(label="Plain Audio")
    audioDecButton = gr.Button("Decode Audio")
    audioDecButton.click(fn=decAudio, inputs=audioInputDec, outputs=audioOutputDec)

    gr.Markdown(margin)

    # IMAGES

    imageSizeW = gr.Number(label="Image Width")
    imageSizeH = gr.Number(label="Image Height")

    imgInputEnc = gr.Image(type="pil", label="Plain Image")
    imgEncodeButton = gr.Button("Encode Image")
    imgEncodeButton.click(
        encodeImage, inputs=[imgInputEnc, imageSizeW, imageSizeH]
    )

    gr.Markdown(margin)

    imgInputDec = gr.UploadButton(label="Upload Cipher Image", type="filepath")
    imgEncodeButton = gr.Button("Decode Image")
    imgOutputDec = gr.Image(type="pil", label="Plain Image")
    imgEncodeButtonSave = gr.Button("Save Plain Image")
    imgEncodeButton.click(decodeImage, inputs=imgInputDec, outputs=imgOutputDec)
    imgEncodeButtonSave.click(decodeImageSave, inputs=imgInputDec)

    gr.Markdown(margin)

    # VIDEO

    videoInputEnc = gr.Video(label="Plain Video")
    videoOutputEnc = gr.Textbox(label="Cipher Video")
    videoEncodeButton = gr.Button("Encode Video")
    videoEncodeButton.click(encVideo, inputs=videoInputEnc, outputs=videoOutputEnc)

    gr.Markdown(margin)

    videoInputDec = gr.Textbox(label="Cipher Video")
    videoOutputDec = gr.Video(label="Plain Video")
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
            imgInputDec,
            imgOutputDec,
        ],
        "../flagged_data_points",
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
    print("Press any key to shutdown server...")
    msvcrt.getch()

elif args.run and not args.share:
    demo.launch(prevent_thread_lock=True)
    webbrowser.open("http://127.0.0.1:7860/")
    print("Press any key to shutdown server...")
    msvcrt.getch()
    
elif args.share and not args.run:
    print("No run flag specified.")
    print("Quitting...")
    exit(1)
