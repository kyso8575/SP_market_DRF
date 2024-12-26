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
        // 이미지 컨테이너
        const imgWrapper = document.createElement('div');
        imgWrapper.classList.add('img-wrapper');

        // 이미지
        const img = document.createElement('img');
        img.src = e.target.result;
        img.alt = file.name;
        img.classList.add('preview-img');

        // 파일 이름
        const fileName = document.createElement('span');
        fileName.textContent = `${index + 1}. ${file.name}`;
        fileName.classList.add('preview-filename');

        // 요소 추가
        imgWrapper.appendChild(img);
        imgWrapper.appendChild(fileName);
        previewContainer.appendChild(imgWrapper);
      };
      reader.readAsDataURL(file);
    });
  });
});

  
function confirmDelete() {
  if (confirm("Are you sure you want to delete this product?")) {
    window.location.href = "{% url 'products:product_delete' product.id %}";
  }
}
