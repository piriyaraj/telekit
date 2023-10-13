$(document).ready(function () {
    $("#category-form").on("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission
  
      $.ajax({
        type: "POST",
        url: "/changecategory",
        data: $(this).serialize(), // Serialize form data
        success: function (response) {
            alert(response.message);
        },
        error: function () {
          // Handle any errors that may occur during the AJAX request
        },
      });
    });
  });