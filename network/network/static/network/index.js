function editPost(button) {
  let postContainer = button.closest('.tweet-container');
  let postId = postContainer.querySelector('.tweet').dataset.postId;
  let postContent = postContainer.querySelector('.tweet-content');
  let postDate = postContainer.querySelector('.tweet-date');

  let currentContent = postContent.innerHTML;

  let textarea = document.createElement('textarea');
  textarea.classList.add('form-control');
  textarea.value = currentContent;

  postContent.innerHTML = '';
  postContent.appendChild(textarea);

  button.innerHTML = 'Save';
  button.addEventListener('click', function() {
    let newContent = textarea.value;

  const csrfToken = document.getElementById('csrf-token').value;

    fetch(`/posts/${postId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        content: newContent
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        postContent.innerHTML = newContent;
        button.innerHTML = 'Edit';
        let updated_at = data.updated_at;
        postDate.innerHTML = 'updated at: '+ updated_at;

      } else {
        alert('An error occurred while saving the post.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while saving the post.');
    });
  });
}

function likePost(button) {
  let postId = button.dataset.postId;
  let likeSpan = button.querySelector('.like');
  let likeCount = button.querySelector('.like-count');
  
  let likeText = button.parentNode.querySelector('.like-text');

  let csrfToken = document.getElementById('csrf-token').value;
console.log(postId)
  fetch(`posts/${postId}/like`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        likeCount.innerText = data.like_count;
        if (button.classList.contains('liked')) {
          button.classList.remove('liked');
          likeText.style.color = 'white';
          likeText.innerHTML = 'Unlike';
        } else {
          button.classList.add('liked');
          likeText.style.color = 'red';
          likeText.innerHTML = 'Like';
        }
      updateLikeStatus(postId);
      } else {
        console.error('An error occurred while liking the post.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}


function updateLikeStatus(postId) {
  let csrfToken = document.getElementById('csrf-token').value;

  fetch(`/posts/${postId}/likes`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      let likeText = document.querySelector(`[data-post-id="${postId}"] .like-text`);
      if (data.is_liked) {
        likeText.innerHTML = 'Unlike';
        likeText.style.color = 'white';
      } else {
        likeText.innerHTML = 'Like';
        likeText.style.color = 'red';
      }
    } else {
      console.error('An error occurred while fetching the like status.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


// Call this function when the page loads to update the like status
window.addEventListener('load', () => {
  let posts = document.querySelectorAll('.tweet');
  posts.forEach(post => {
    let postId = post.dataset.postId;
    updateLikeStatus(postId);
  });
});


