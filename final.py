from flask import *
import mysql.connector
import cv2
import torch
import os
import numpy as np
from torchvision import transforms
from facenet_pytorch import MTCNN, InceptionResnetV1
import time
import pickle
from PIL import Image
from random import *
from email_otp import *

app = Flask(__name__)
app.secret_key = 'EmailAuthenticationByShivamYadav2021'
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="info")
mycursor = mydb.cursor()


# Initialize thermal camera or import library if available
def capture_thermal_image():
    # Import necessary libraries
    import your_thermal_camera_library
    
    # Initialize and configure your thermal camera
    camera = your_thermal_camera_library.ThermalCamera()
    camera.connect()  # Connect to the camera
    
    # Capture a thermal image
    thermal_image = camera.capture_image()
    
    # Disconnect from the camera
    camera.disconnect()
    
    return thermal_image



def preprocess_thermal_image(thermal_image):
    # Example preprocessing steps:
    
    # Resize the image to the desired dimensions
    resized_image = cv2.resize(thermal_image, (new_width, new_height))

    # Normalize pixel values if necessary
    normalized_image = cv2.normalize(resized_image, None, 0, 255, cv2.NORM_MINMAX)

    # Convert the image to grayscale if needed
    grayscale_image = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2GRAY)

    # Perform any additional preprocessing steps as required
    
    return grayscale_image



@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('training.html')


@app.route("/logi")
def logi():
    return render_template('login.html')


@app.route("/AtmLogin")
def AtmlLogin():
    return render_template('atmlogin.html')


@app.route("/adlog")
def adlog():
    return render_template("admin.html")


@app.route('/val', methods=['GET', 'POST'])
def val():
    if request.method == 'POST':
        if request.form.get('username') == 'abc' and request.form.get('password') == '123':
            return render_template('admin.html')
        else:
            return render_template('login.html', msg='Invalid Username or Password')

    else:
        return render_template('login.html')


@app.route("/Admin", methods=['GET', 'POST'])
def Admin():
    if request.method == 'POST':
        card = request.form['name']
        un = request.form['ename']
        email = request.form['email']

        insertQuery = "INSERT INTO facetb VALUES ('" + card + "','" + un + "','" + email + "')"
        mycursor.execute(insertQuery)
        mydb.commit()

        image_size = 600
        frame_rate = 64
        vid_len = 20
        device = torch.device(
            "cuda" if torch.cuda.is_available()
            else "cpu")

        def save_face_images(frames, boxes):
            transform = transforms.Compose([
                transforms.Resize((160, 160)),
                transforms.ToTensor()
            ])
            for f in range(len(frames)):
                img = np.asarray(frames[f])
                box = boxes[f]
                if len(box.shape) == 3:
                    for b in range(box.shape[1]):
                        start = (np.clip(int(box[0][b][0]) - 15, 0, 480), np.clip(int(box[0][b][1]) - 50, 0, 640))
                        end = (np.clip(int(box[0][b][2]) + 15, 0, 480), np.clip(int(box[0][b][3]) + 20, 0, 640))
                        crop_pic = img[start[1]:end[1], start[0]:end[0]]
                    img_crop = Image.fromarray(crop_pic)
                    img_crop = transform(img_crop)
                    img_crop = torch.unsqueeze(img_crop, 0)
                    save_tensor = model(img_crop)
                    return save_tensor

        v_cap = cv2.VideoCapture(0)
        v_cap.set(cv2.CAP_PROP_FRAME_WIDTH, image_size)
        v_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, image_size)
        count = 1
        prev = 0
        try:
            os.mkdir(card)
        except FileExistsError:
            pass

        mtcnn = MTCNN(image_size=image_size, keep_all=True, device=device, post_process=True)
        model = InceptionResnetV1(pretrained='vggface2', classify=False).eval()
        start = time.time()
        frames = []
        boxes = []
        print(
            'Try to keep your face at the centre of the screen and turn ur face slowly in order to capture diff angles of your face')
        time.sleep(3)
        print('A window will pop up in abt 3 seconds')
        time.sleep(3)
        save_tensor = None

        while True:
            time_elapsed = time.time() - prev
            curr = time.time()
            if curr - start >= vid_len:
                break
            ret, frame = v_cap.read()
            cv2.imshow('Recording and saving Images', frame)
            if time_elapsed > 1. / frame_rate:
                prev = time.time()
                frame_ = Image.fromarray(frame)
                frames.append(frame_)
                batch_boxes, prob, landmark = mtcnn.detect(frames, landmarks=True)
                frames_duplicate = frames.copy()
                boxes.append(batch_boxes)
                boxes_duplicate = boxes.copy()
                if save_tensor is None:
                    save_tensor = save_face_images(frames_duplicate, boxes_duplicate)
                else:
                    temp = save_face_images(frames_duplicate, boxes_duplicate)
                    if temp is not None:
                        save_tensor = torch.cat([temp, save_tensor], dim=0)
                        print(save_tensor.shape)
                count += 1
                frames = []
                boxes = []
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        face_file = open(card + '/' + un, 'ab')
        pickle.dump(save_tensor, face_file)
        face_file.close()
        v_cap.release()
        cv2.destroyAllWindows()

        return render_template('facecam.html')


@app.route('/face', methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        card_number = request.form.get('card')

        transform = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.ToTensor()
        ])

        frame_rate = 16
        prev = 0
        batch_size = 32
        image_size = 600
        threshold = 0.85
        device = torch.device(
            "cuda" if torch.cuda.is_available()
            else "cpu")
        bbx_color = (0, 255, 255)

        current_person = None

        def detect_imgs(img):
            global current_person
            person_ = None
            img = transform(img)
            img = torch.unsqueeze(img, 0)
            img = model(img)
            minimum = torch.tensor(99)
            for face_, name in zip(faces, face_names):
                temp = torch.min(torch.norm((face_ - img), dim=1))
                if temp < minimum and temp < threshold:
                    minimum = temp
                    person_ = name
                    current_person = name
            return person_, minimum.item()

        def show_images(frames, boxes, color):
            temp = None
            for f in range(len(frames)):
                img = np.asarray(frames[f])
                box = boxes[f]
                if len(box.shape) == 3:
                    for b in range(box.shape[1]):
                        start = (np.clip(int(box[0][b][0]) - 15, 0, 600), np.clip(int(box[0][b][1]) - 20, 0, 600))
                        end = (np.clip(int(box[0][b][2]) + 15, 0, 600), np.clip(int(box[0][b][3]) + 15, 0, 600))
                        img = cv2.rectangle(cv2.UMat(img), start, end, color, 2)  # Convert to cv::UMat
                        crop_pic = img.get()  # Convert back to NumPy array
                        crop_pic = crop_pic[start[1]:end[1], start[0]:end[0]]
                        crop_pic = Image.fromarray(crop_pic)
                        person, diff = detect_imgs(crop_pic)
                        if person is not None:
                            cv2.putText(img, person + ': ' + '{:.2f}'.format(diff), (start[0], start[1] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
                            temp = 1
                        else:
                            cv2.putText(img, 'Unknown' + ': ' + '{0}'.format(diff), (start[0], start[1] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
                            temp = 0
                cv2.imshow('Detection', img)
                if temp == 1:
                    return 1
                else:
                    return 0


        mtcnn = MTCNN(image_size=image_size, keep_all=True, device=device, post_process=True)
        model = InceptionResnetV1(pretrained='vggface2', classify=False).eval()

        frames = []
        boxes = []

        faces = []
        face_names = []
        face_file = None
        try:
            for person in os.listdir(card_number):
                face_file = open(card_number + '/' + person, 'rb')
                if face_file is not None:
                    face = pickle.load(face_file)
                    faces.append(face)
                    face_names.append(str(person))
        except FileNotFoundError:
            print('Face data doesnt exist for this card.')
            exit()

        v_cap = cv2.VideoCapture(0)
        v_cap.set(cv2.CAP_PROP_FRAME_WIDTH, image_size)
        v_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, image_size)
        flag = False
        face_results = []
        start = time.time()
        while (True):
            time_elapsed = time.time() - prev
            break_time = time.time() - start
            if break_time > 10:
                break
            ret, frame = v_cap.read()
            if time_elapsed > 1. / frame_rate:
                prev = time.time()
                frame_ = Image.fromarray(frame)
                frames.append(frame_)
                batch_boxes, prob, landmark = mtcnn.detect(frames, landmarks=True)
                frames_duplicate = frames.copy()
                boxes.append(batch_boxes)
                boxes_duplicate = boxes.copy()
                face_results.append(show_images(frames_duplicate, boxes_duplicate, bbx_color))
                frames = []
                boxes = []
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        v_cap.release()
        cv2.destroyAllWindows()
        accuracy = (sum(face_results) / len(face_results)) * 100
        print('Percentage match ' + '{:.2f}'.format(accuracy))
        if accuracy > 10:
            print('Authorization Successful')
            sql = "SELECT email FROM `facetb` WHERE `card` =%s "
            val = (card_number,)
            mycursor.execute(sql, val)
            account = mycursor.fetchone()
            acc = account[0]
            current_otp = sendEmailVerificationRequest(receiver=acc)
            session['current_otp'] = current_otp
            return render_template('verify.html')
        else:
            print('Authorization Unsuccessful')
            return render_template('Unauthorization.html')
            quit()


@app.route('/validate', methods=["POST"])
def validate():
    current_user_otp = session['current_otp']
    user_otp = request.form['otp']
    if int(current_user_otp) == int(user_otp):
        return render_template('voting.html')
    else:
        return "<h3> Oops! Email Verification Failure, OTP does not match. </h3>"


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        cname = request.form.get('name')
        sql = 'SELECT * FROM `counts` WHERE `name` = %s'
        val = (cname,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result:
            for row in result:
                num = int(row[2])
                sql1 = 'UPDATE `counts` SET `count` = %s WHERE `name` = %s'
                val1 = (num + 1, cname)
                mycursor.execute(sql1, val1)
                mydb.commit()
                return render_template('success.html', msg='Vote Added Successfully')
        else:
            return 'No Data'


@app.route('/count')
def count():
    sql = "SELECT * FROM `counts`"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template('count.html', data=result)


@app.route('/view')
def view():
    sql = "SELECT * FROM facetb"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return render_template('view.html', data=result)


@app.route('/capture_thermal', methods=['GET', 'POST'])
def capture_thermal():
    if request.method == 'POST':
        thermal_image = capture_thermal_image()
        if thermal_image is not None:
            processed_thermal_image = preprocess_thermal_image(thermal_image)
            # Pass the processed thermal image to your facial recognition function
            # Perform facial recognition on the processed image and proceed accordingly
        else:
            return "Failed to capture thermal image"
    return render_template('capture_thermal.html')


if __name__ == '__main__':
    app.run(debug=True, port=2000)
