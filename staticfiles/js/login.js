async function login() {
  let fd = getDataFromMessageForm();
  try {
    showLoadingAnimation();
    let json = await waitingForServerResponse(fd);
    showLoginSuccess(json);
  }
  catch (e) {
    removeLoadingAnimation();
    showLoginFailed();
  }
}

function getDataFromMessageForm() {
  let fd = new FormData();
  fd.append('username', username.value);
  fd.append('password', password.value);
  fd.append('csrfmiddlewaretoken', token);
  return fd;
}

async function waitingForServerResponse(fd) {
  let response = await fetch('/login/', {
    method: 'POST',
    body: fd
  });

  return await response.json();
}

function showLoginSuccess(json) {
  removeLoadingAnimation();
  window.location.href = `${json['RedirectTo']}`;
}

function showLoginFailed() {
  showPasswordOrUsernameWrong();
}

function showPasswordOrUsernameWrong() {
  document.getElementById('error').classList.remove('d-none');
}
function hidePasswordOrUsernameWrong() {
  document.getElementById('error').classList.add('d-none');
}
function showLoadingAnimation() {
  username.disabled = true;
  password.disabled = true;
  hidePasswordOrUsernameWrong();
  document.getElementById('spinner').classList.remove('d-none');
}
function removeLoadingAnimation() {
  username.disabled = false;
  password.disabled = false;
  document.getElementById('spinner').classList.add('d-none');
}