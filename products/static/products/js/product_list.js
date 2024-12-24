document.addEventListener('DOMContentLoaded', () => {
  const likeButtons = document.querySelectorAll('.like-button');

  likeButtons.forEach(button => {
      button.addEventListener('click', () => {
          const productId = button.getAttribute('data-product-id');
          const likeCountElement = document.querySelector(`.like-count[data-product-id="${productId}"]`);

          fetch(`/products/like/${productId}/`, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCSRFToken(),
                  'X-Requested-With': 'XMLHttpRequest',
              },
          })
          .then(response => response.json())
          .then(data => {
              if (data.status === 'liked') {
                  button.innerHTML = '❤️';
                  button.classList.add('liked');
              } else {
                  button.innerHTML = '🤍';
                  button.classList.remove('liked');
              }
              likeCountElement.innerText = data.likes_count;
          })
          .catch(error => console.error('Error:', error));
      });
  });
});

function getCSRFToken() {
  const csrfTokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return csrfTokenElement ? csrfTokenElement.value : '';
}
