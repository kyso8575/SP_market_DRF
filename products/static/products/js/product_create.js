document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('images');
    const previewContainer = document.getElementById('image-preview');
  
    imageInput.addEventListener('change', function () {
      // 기존 미리보기 초기화
      previewContainer.innerHTML = '';
  
      const files = imageInput.files;
  
      if (files.length === 0) {
        return; // 선택된 파일이 없으면 종료
      }
  
      // 파일 목록 순서대로 처리
      Array.from(files).forEach((file, index) => {
        // 파일이 이미지인지 확인
        if (!file.type.startsWith('image/')) {
          alert('이미지 파일만 업로드할 수 있습니다!');
          return; // 다음 파일로 넘어감
        }
  
        const reader = new FileReader();
        reader.onload = function (e) {
          // 이미지 미리보기 및 파일 이름 표시
          const imgWrapper = document.createElement('div');
          imgWrapper.style.display = 'flex';
          imgWrapper.style.alignItems = 'center';
          imgWrapper.style.marginBottom = '10px';
  
          // 이미지 미리보기
          const img = document.createElement('img');
          img.src = e.target.result;
          img.alt = file.name;
          img.style.width = '100px';
          img.style.height = '100px';
          img.style.objectFit = 'cover';
          img.style.border = '1px solid #ccc';
          img.style.borderRadius = '5px';
          img.style.marginRight = '10px';
  
          // 파일 이름 표시
          const fileName = document.createElement('span');
          fileName.textContent = `${index + 1}. ${file.name}`;
          fileName.style.fontWeight = 'bold';
          fileName.style.fontSize = '14px';
  
          // 요소 추가
          imgWrapper.appendChild(img);
          imgWrapper.appendChild(fileName);
          previewContainer.appendChild(imgWrapper);
        };
        reader.readAsDataURL(file);
      });
    });
  });
  