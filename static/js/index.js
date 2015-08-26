$(document).ready(function() {
  $('option[value=en]').prop('selected', true);
  $('input[name=text]').focus();

  $('#sound-form').isHappy({
    fields: {
      '#input-text': {
        message: 'Input is over 100 characters! It will be truncated.',
        test: validateLength,
        trim: false,
        when: 'input keyup'
      },
    }
  });

  function validateLength(text) {
    return text.length <= 100;
  }

  $('body').on('click', 'button.play', function() {
    var audio = $(this).siblings('audio');
    audio.trigger('play');
  });

  $('body').on('click', 'button.save', function() {
    window.open( $(this).data('sound'), '_blank' );
  });

  $('#submit-text').on('click', function(e) {
    e.preventDefault();

    if ( $('#input-text').val().length === 0) {
      // don't submit if input text is empty
      return false;
    }

    var data = $('.content form').serialize();

    requestSound(data)

    // clear input box
    $('.content input[name=text]').val('');
    $('.content input[name=text]').keyup(); // satisfy isHappy
  });

  $('body').on('click', '#submit-captcha', function(e) {
    e.preventDefault();

    if ( $('#input-captcha').val().length === 0) {
      return false;
    }

    var data = $('.captcha form').serialize();

    $.ajax({
      type: 'POST',
      url: '/captcha',
      data: data,
      success: captchaSuccess,
      error: function() {
        showError( 'Unable to submit captcha. '
                 + 'Please send me an email if this continues to occur.'
                 );
      }
    });
  });

  function requestSound(data) {
    $.ajax({
      type: 'POST',
      url: '/sounds',
      data: data,
      success: loadResult,
      error: function() {
        showError( 'Unable to create that sound. '
                 + 'Please send me an email if this continues to occur.'
                 );
      }
    });
  }

  function loadResult(res) {
    if (res.success) {
      getSound(res.id);
    } else {
      showWarning( 'Please fill out the captcha in order to continue.' );
      $('.wrapped.captcha').remove()
      $('.content').after(res.template)
    }
  }

  function getSound(id) {
    $.ajax({
      type: 'GET',
      url: '/sounds/' + id,
      success: showSound,
      error: function() {
        showError( 'Unable to retrieve sound. '
                 + 'Please send me an email if this continues to occur.'
                 );
      }
    });
  }

  function showSound(res) {
    if ( $('#results').length == 0 ) {
      showResults(res);
    } else {
      $('#results').prepend(res);
    }
  }

  function showResults(child) {
    $.ajax({
      type: 'GET',
      url: '/results',
      success: function(res) {
        $('.content').after(res);
        $('#results').prepend(child);
      },
      error: function() {
        showError( 'Something really bad happened. '
                 + 'You should probably reload the page. '
                 + 'Please send me an email if this continues to occur.'
                 );
      }
    });
  }

  function captchaSuccess(res) {
    $('.wrapped.captcha').remove()

    if (res.success) {
      requestSound({
        lang: res.lang,
        text: res.text
      });
    } else {
      loadResult(res)
    }
  }

  function showError(text) {
    noty({
      layout: 'top',
      theme: 'relax',
      type: 'error',
      text: text,
      killer: true
    });
  }

  function showWarning(text) {
    noty({
      layout: 'top',
      theme: 'relax',
      type: 'warning',
      text: text,
      killer: true
    })
  }
});
