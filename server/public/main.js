$(function () {
  const FADE_TIME = 150 // ms
  const TYPING_TIMER_LENGTH = 400 // ms
  const FEEDBACK = true
  const COLORS = [
    '#e21400', '#91580f', '#f8a700', '#f78b00',
    '#58dc00', '#287b00', '#a8f07a', '#4ae8c4',
    '#3b88eb', '#3824aa', '#a700ff', '#d300e7'
  ]

  const EMOTION_COLORS = {
    neutral: '#767676',
    sadness: '#2185D0',
    happiness: '#21BA45',
    worry: '#F2711C',
    surprise: '#FBBD08',
    love: '#E03997',
    hate: '#A5673F',
    fun: '#A333C8',
    relief: '#00B5AD',
    enthusiasm: '#B5CC18',
    boredom: '#6435C9',
    empty: '#1B1C1D'
  }

    // Initialize letiables
  const $window = $(window)
  const $usernameInput = $('.usernameInput') // Input for username
  const $messages = $('.messages') // Messages area
  const $inputMessage = $('.inputMessage') // Input message input box

  const $loginPage = $('.login.page') // The login page
  const $chatPage = $('.chat.page') // The chatroom page

    // Prompt for setting a username
  let username
  let connected = false
  let typing = false
  let lastTypingTime
  let $currentInput = $usernameInput.focus()



  const socket = io()
    // Keyboard events

  $window.keydown(event => {
        // Auto-focus the current input when a key is typed
    if (!(event.ctrlKey || event.metaKey || event.altKey)) {
      $currentInput.focus()
    }
        // When the client hits ENTER on their keyboard
    if (event.which === 13) {
      if (username) {
        sendMessage()
        socket.emit('stop typing')
        typing = false
      } else {
        setUsername()
      }
    }
  })

  $inputMessage.on('input', updateTyping)

    // Focus input when clicking anywhere on login page
  $loginPage.click(() => $currentInput.focus())

    // Focus input when clicking on the message input's border
  $inputMessage.click(() => $inputMessage.focus())

    // Socket events

    // Whenever the server emits 'login', log the login message
  socket.on('login', data => {
    connected = true
        // Display the welcome message
    const message = `Welcome to EmotionChat – write in English to be analyzed!`
    log(message, {
      prepend: true
    })
    addParticipantsMessage(data)
  })

    // Whenever the server emits 'new message', update the chat body
  socket.on('new message', function (data) {
    addChatMessage(data)
  })

    // Whenever the server emits 'user joined', log it in the chat body
  socket.on('user joined', function (data) {
    log(`${data.username} joined`)
    addParticipantsMessage(data)
  })

    // Whenever the server emits 'user left', log it in the chat body
  socket.on('user left', data => {
    log(`${data.username} left`)
    addParticipantsMessage(data)
    removeChatTyping(data)
  })

    // Whenever the server emits 'typing', show the typing message
  socket.on('typing', addChatTyping)

    // Whenever the server emits 'stop typing', kill the typing message
  socket.on('stop typing', removeChatTyping)

  socket.on('disconnect', () => log('you have been disconnected'))

  socket.on('reconnect', () => {
    log('you have been reconnected')
    if (username) {
      socket.emit('add user', username)
    }
  })

  socket.on('reconnect_error', () => log('attempt to reconnect has failed'))

  socket.on('emotion', data => {
    $(`#${data.localId}`).append(createEmotionDiv(data.emotion))
  })

    // Prevents input from having injected markup
  function cleanInput (input) {
    return $('<div/>').text(input).text()
  }

  function addParticipantsMessage (data) {
    log(data.numUsers === 1 ? "there's 1 participant" : `there are ${data.numUsers} participants`)
  }

    // Sets the client's username
  function setUsername () {
    username = cleanInput($usernameInput.val().trim())

        // If the username is valid
    if (!username) return

    $loginPage.fadeOut()
    $chatPage.show()
    $loginPage.off('click')
    $currentInput = $inputMessage.focus()

        // Tell the server your username
    socket.emit('add user', username)
  }

    // Adds a message element to the messages and scrolls to the bottom
    // el - The element to add as a message
    // options.fade - If the element should fade-in (default = true)
    // options.prepend - If the element should prepend
    //   all other messages (default = false)
  function addMessageElement (el, { fade = true, prepend = false } = {}) {
    const $el = $(el)

    if (fade) {
      $el.hide().fadeIn(FADE_TIME)
    }
    if (prepend) {
      $messages.prepend($el)
    } else {
      $messages.append($el)
    }
    $messages[0].scrollTop = $messages[0].scrollHeight
  }

    // Log a message
  function log (message, options) {
    const $el = $('<li>').addClass('log').text(message)
    addMessageElement($el, options)
  }
  let localId = 0
    // Adds the visual chat message to the message list
  function addChatMessage (data, options = {}) {
        // Don't fade the message in if there is an 'X was typing'
    const $typingMessages = getTypingMessages(data)

    if ($typingMessages.length !== 0) {
      options.fade = false
      $typingMessages.remove()
    }

    const $usernameDiv = $('<span class="username"/>')
            .text(data.username)
            .css('color', getUsernameColor(data.username))

    const $messageBodyDiv = $(`<span class="messageBody"/>`)
            .text(data.message)

    const typingClass = data.typing ? 'typing' : ''
    const $messageDiv = $(`<li class="message" id="${++localId}"/>`)
            .data('username', data.username)
            .addClass(typingClass)
            .append($usernameDiv, $messageBodyDiv)

    if (data.emotion) $messageDiv.append(createEmotionDiv(data.emotion))

    addMessageElement($messageDiv, options)
  }

    // Adds the visual chat typing message
  function addChatTyping (data) {
    data.typing = true
    data.message = 'is typing'
    addChatMessage(data)
  }

    // Updates the typing event
  function updateTyping () {
    if (connected) {
      if (!typing) {
        typing = true
        socket.emit('typing')
      }
      lastTypingTime = (new Date()).getTime()

      setTimeout(function () {
        const typingTimer = (new Date()).getTime()
        const timeDiff = typingTimer - lastTypingTime
        if (timeDiff >= TYPING_TIMER_LENGTH && typing) {
          socket.emit('stop typing')
          typing = false
        }
      }, TYPING_TIMER_LENGTH)
    }
  }

  function sendFeedback (text, emotion) {
    const data = JSON.stringify({text, emotion})
    console.log(`sending feedback: ${data}`)
    socket.emit('feedback', data)
  }

    // Gets the 'X is typing' messages of a user
  function getTypingMessages (data) {
    return $('.typing.message').filter(function (i) {
      return $(this).data('username') === data.username
    })
  }

    // Gets the color of a username through our hash function
  function getUsernameColor (username) {
        // Compute hash code
    let hash = 7
    for (let i = 0; i < username.length; i++) {
      hash = username.charCodeAt(i) + (hash << 5) - hash
    }
        // Calculate color
    const index = Math.abs(hash % COLORS.length)
    return COLORS[index]
  }

    // Removes the visual chat typing message
  function removeChatTyping (data) {
    getTypingMessages(data).fadeOut(function () {
      $(this).remove()
    })
  }

  function setEmotionButton (emotionButton, emotion) {
      emotionButton.text(emotion)
              .css('background-color', EMOTION_COLORS[emotion])
  }

  function createEmotionDiv (emotion) {
    const $emotionDiv = $(`<div class="emotionDiv"/>`)

    const $emotionButton = $(`<button class="emotion"/>`)
    setEmotionButton($emotionButton, emotion)

    const $emotionHover = $(`<div class="emotionHover"/>`)
            .hide()

    for (const key in EMOTION_COLORS) {
      const $emotionValue = $(`<button class="emotion"/>`)
                .text(key)
                .css('background-color', EMOTION_COLORS[key])
                .click(event => {
                  const target = $(event.target)
                  setEmotionButton($emotionButton, key)
                  const $message = target.closest('li.message')
                  const $messageBody = $message.children('.messageBody')
                  sendFeedback($messageBody.text(), key)
                  $message.children('.emotionDiv').children().toggle()
                })
      $emotionHover.append($emotionValue)
    }

    $emotionDiv.append($emotionButton)

    if (FEEDBACK) {
      $emotionDiv.append($emotionHover)

      $emotionDiv.mouseover(function () {
        $emotionButton.hide()
        $emotionHover.show()
        //$(this).children().toggle()
      })
      $emotionDiv.mouseout(function () {
        $emotionButton.show()
        $emotionHover.hide()
        //$(this).children().toggle()
      })
    }
    return $emotionDiv
  }

    // Sends a chat message
  function sendMessage () {
    let message = $inputMessage.val()

        // Prevent markup from being injected into the message
    message = cleanInput(message)

        // if there is a non-empty message and a socket connection
    if (!message || !connected) return

    $inputMessage.val('')

    addChatMessage({
      username: username,
      message: message
    })

        // tell server to execute 'new message' and send along one parameter
    socket.emit('new message', {message, localId})
  }
})
