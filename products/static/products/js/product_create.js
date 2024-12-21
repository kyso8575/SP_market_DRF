document.addEventListener('DOMContentLoaded', () => {
  const imageInput = document.getElementById('images');
  const previewContainer = document.getElementById('image-preview');

  imageInput.addEventListener('change', function () {
      // 기존 미리보기 초기화
      previewContainer.innerHTML = '';

      // 첫 번째 파일만 사용
      const file = imageInput.files[0];

      if (!file) {
          return; // 선택된 파일이 없으면 종료
      }

      // 파일이 이미지인지 확인
      if (!file.type.startsWith('image/')) {
          alert('Only image files are allowed!');
          return;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
          // 이미지 미리보기 요소 생성
          const img = document.createElement('img');
          img.src = e.target.result;
          img.alt = 'Selected Image';
          img.style.width = '200px';
          img.style.height = '200px';
          img.style.objectFit = 'cover';
          img.style.border = '1px solid #ccc';
          img.style.borderRadius = '5px';
          previewContainer.appendChild(img);
      };
      reader.readAsDataURL(file);
  });
});
