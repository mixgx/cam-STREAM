from flask import Flask, render_template, Response, request, send_file, redirect, jsonify
import cv2
import os
app = Flask(__name__)
global camera
global onuse
global rec
global outrec
global vlip

vlip = open('vlip', 'r').read().split(' ')
rec = 'no_rec'
onuse = None
camera = None#cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outrec = None


def add_ip(ip):
    global vlip
    to_add = open('vlip', 'r').read()
    open('vlip', 'w').write(to_add+' '+ip)
    vlip = open('vlip', 'r').read().split(' ')
    
def clear_ip():
    global vlip
    open('vlip', 'w').write('')
    vlip = open('vlip', 'r').read().split(' ')
            
def test_ip(ip):
    for ips in vlip:
        if ip == ips:
            return True        
    return False
            
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        try:
            outrec.write(frame)
        except:
            pass
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
def gen_image():
    count = open('count', 'r').read().split(' ')
    try:
        success, frame = camera.read()  # read the camera frame
        out = cv2.imwrite('pic/image'+count[1]+'.jpg', frame)
        open('count', 'w').write(count[0]+' '+(str(int(count[1])+1)))
        return 'OK'
    except:
        return 'Camera not online'
    

@app.route('/')
def home():
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        return render_template('home.html')
    else:
        return render_template('not_ip.html')
    

@app.route('/cam')
def cam():
    global rec
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        new_onuse = request.args.get('cam')
        if new_onuse == None:
            pass
        else:
            onuse = new_onuse
        #print(onuse)
        return render_template('index.html', rec=rec)
    else:
        return render_template('not_ip.html')
    
@app.route('/make_pic')
def make_pic():
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        gen_image()
        return redirect("/cam")
    else:
        return render_template('not_ip.html')
    
@app.route('/start_rec')
def rec():
    global rec
    global outrec
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        rec = 'rec'
        count = open('count', 'r').read().split(' ')
        outrec = cv2.VideoWriter('records/output'+count[0]+'.avi',fourcc, 20.0, (640,480))
        open('count', 'w').write((str(int(count[0])+1))+' '+count[1])
        return redirect("/cam")
    else:
        return render_template('not_ip.html')
    
@app.route('/stop_rec')
def norec():
    global rec
    global outrec
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        try:
            outrec.release()
        except:
            pass
        rec = 'no_rec'
        return redirect("/cam")
    else:
        return render_template('not_ip.html')

@app.route('/pic')
def pic():
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        path = './pic'
        entries = os.listdir(path)
        print(entries.reverse())
        return render_template('pic.html', pics=entries)
    else:
        return render_template('not_ip.html')
    
@app.route('/get_ip')
def get_user_ip():
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        return request.remote_addr
    else:
        return render_template('not_ip.html')

@app.route('/vid')
def vid():
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        path = './records'
        entries = os.listdir(path)
        print(entries.reverse())
        return render_template('vid.html', vids=entries)
    else:
        return render_template('not_ip.html')
    
@app.route("/<path>/<name>")
def download_pic(path, name):
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        return send_file(path+'\\'+name)
    else:
        return render_template('not_ip.html')
    
@app.route('/on')
def on():
    global camera
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        camera = cv2.VideoCapture(0)
        return '<meta http-equiv="refresh" content="1;URL=/cam" /> OK'
    else:
        return render_template('not_ip.html')

@app.route('/off')
def off():
    global camera
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        camera.release()
        return '<meta http-equiv="refresh" content="1;URL=/cam" /> OK'
    else:
        return render_template('not_ip.html')

@app.route('/video_feed')
def video_feed():
    global vlip
    vlip = open('vlip', 'r').read().split(' ')
    if test_ip(request.remote_addr):
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return render_template('not_ip.html')
        
@app.route('/seq_addmyip')#, methods=['POST'])
def addmyip():
    return render_template('add_ip.html', your_ip=request.remote_addr)
    
@app.route('/final_add_the_ip_hah', methods=['POST'])
def wow_addmyip():
    ip = request.form.get("ip")
    password = request.form.get("pass")    
    if password == 'wasdx':
        add_ip(ip)
    else:
        pass
    return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.220', port=80)
