// 1. 文件选择反馈逻辑
function handleFileSelect(input) {
    const fileNameText = document.getElementById('file-name-text');
    const uploadZone = document.getElementById('drop-zone');

    if (input.files && input.files[0]) {
        fileNameText.innerHTML = `已选择: <strong>${input.files[0].name}</strong>`;
        fileNameText.style.color = "#4CAF50";
        uploadZone.classList.add('has-file');
    }
}

// 2. 摄像头逻辑 (保持你之前的代码不变)
const startCameraBtn = document.getElementById('start-camera-btn');
const cameraContainer = document.getElementById('camera-container');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture-btn');
const closeCameraBtn = document.getElementById('close-camera-btn');
const photoPreview = document.getElementById('photo-preview');
const previewImg = document.getElementById('preview-img');
const submitPhotoBtn = document.getElementById('submit-photo-btn');
let stream = null;

function checkCameraAvailability() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("当前环境无法调用摄像头！请确保使用HTTPS或localhost访问。");
        return false;
    }
    return true;
}

startCameraBtn.addEventListener('click', async () => {
    if (!checkCameraAvailability()) return;
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        video.srcObject = stream;
        cameraContainer.style.display = 'block';
        startCameraBtn.style.display = 'none';
    } catch (err) {
        alert("无法访问摄像头：" + err.message);
    }
});

captureBtn.addEventListener('click', () => {
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    previewImg.src = canvas.toDataURL('image/jpeg');
    photoPreview.style.display = 'block';
});

closeCameraBtn.addEventListener('click', () => {
    if (stream) stream.getTracks().forEach(track => track.stop());
    cameraContainer.style.display = 'none';
    startCameraBtn.style.display = 'block';
});

submitPhotoBtn.addEventListener('click', async () => {
    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'camera_photo.jpg');
        const response = await fetch(window.location.href, { method: 'POST', body: formData });
        const html = await response.text();
        document.open(); document.write(html); document.close();
    }, 'image/jpeg');
});
// static/js/script.js

function handleFileSelect(input) {
    const placeholder = document.getElementById('upload-placeholder');
    const previewContainer = document.getElementById('preview-container');
    const previewImage = document.getElementById('image-preview-element');
    const uploadZone = document.getElementById('drop-zone');

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        // 当文件读取完成时触发
        reader.onload = function(e) {
            // 1. 将读取到的图片地址赋给 img 标签
            previewImage.src = e.target.result;

            // 2. 隐藏提示文字，显示预览图
            placeholder.style.display = 'none';
            previewContainer.style.display = 'block';

            // 3. 增加视觉反馈
            uploadZone.classList.add('has-file');
        };

        reader.readAsDataURL(input.files[0]); // 读取文件内容
    }
}
function switchTab(tabId, btn) {
    // 1. 隐藏所有选项卡内容
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    // 2. 移除所有按钮的 active 类
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(b => b.classList.remove('active'));

    // 3. 显示当前选中的内容，并激活对应按钮
    document.getElementById(tabId).classList.add('active');
    btn.classList.add('active');
}