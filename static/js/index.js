$(document).ready(function() {
  var $input = $('#input-text');
  var maxCharacters = 100;
  var $form = $('#sound-form');
  var $errorMessage = $('<span id="input-text_unhappy" class="unhappyMessage" style="display: none;" role="alert">Input is over ' + maxCharacters + ' characters! It will be truncated.</span>').appendTo($input.parent());
  var selectedLanguage = 'en';

  if (window.localStorage) {
    // Store language preference when the select changes
    $('select[name="lang"]').on('change', function(e) {
      window.localStorage.setItem('sot-lang', $(this).val());
    });

    // Get current preference, if any
    if (window.localStorage.getItem('sot-lang')) {
      selectedLanguage = window.localStorage.getItem('sot-lang');
    }
  }

  // Set default or preferred language
  $('option[value=' + selectedLanguage + ']').prop('selected', true);

  $input
    // Set focus to main text input
    .focus()
    // Validate entries
    .on('keyup input', function _onInputEntry (/*e*/) {
      if (!validateLength($input.val())) {
        // Show error message
        $errorMessage.show();
      }
      else {
        // Hide error message
        $errorMessage.hide();
      }
    });

  function validateLength(text) {
    return text.length <= maxCharacters;
  }

  $('body').on('click', 'button.play', function() {
    var audio = $(this).siblings('audio');
    audio.trigger('play');
  });

  $('body').on('click', 'button.save', function() {
    window.open( $(this).data('sound'), '_blank' );
  });

  $form.on('submit', function(e) {
    e.preventDefault();

    // don't submit if input text is empty or too long
    if (!$input.val().trim().length || !validateLength($input.val())) {
      return false;
    }

    var data = $form.serialize();

    requestSound(data)

    // clear input box
    $input.val('');
    $input.keyup(); // satisfy validation
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
