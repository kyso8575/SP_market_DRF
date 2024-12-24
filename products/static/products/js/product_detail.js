document.addEventListener('DOMContentLoaded', () => {
  const likeForm = document.getElementById('like-form');
  const likeButton = document.getElementById('like-button');
  const likesCount = document.getElementById('likes-count');

  likeForm.addEventListener('submit', (event) => {
    event.preventDefault(); // 기본 Form 제출 방지

    fetch(likeForm.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'liked') {
        likeButton.classList.add('active');
        likeButton.textContent = 'Remove from Wishlist';
      } else {
        likeButton.classList.remove('active');
        likeButton.textContent = 'Add to Wishlist';
      }
      likesCount.textContent = data.likes_count;
    })
    .catch(error => console.error('Error:', error));
  });
});
