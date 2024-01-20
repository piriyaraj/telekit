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

function addToProfile(linkElement) {
  event.preventDefault();

  // Get the link ID from the data attribute
  var linkId = $(linkElement).data("linkid");

  // AJAX request to add the link to the user's profile
  $.ajax({
    type: "GET",
    url: "/addlinkprofile/" + linkId,
    success: function (response) {
      // Handle the response, e.g., show a success message
      alert(response.message);
      console.log(response.message);
      $(linkElement).text("Remove from profile");
      $(linkElement).attr("onclick", "removeToProfile(this);");
      $(linkElement).css("backgroundColor", "#461212");
    },
    error: function (error) {
      // Handle the error, e.g., show an error message
      console.error(error);
    },
  });
}
function removeToProfile(linkElement) {
  event.preventDefault();

  // Get the link ID from the data attribute
  var linkId = $(linkElement).data("linkid");

  // AJAX request to add the link to the user's profile
  $.ajax({
    type: "GET",
    url: "/removelinkprofile/" + linkId,
    success: function (response) {
      // Handle the response, e.g., show a success message
      alert(response.message);
      console.log(response.message);
      $(linkElement).text("Add to profile");
      $(linkElement).attr("onclick", "addToProfile(this);");

      $(linkElement).css("backgroundColor", "#0088cc");
    },
    error: function (error) {
      // Handle the error, e.g., show an error message
      console.error(error);
    },
  });
}
function change18plus(linkElement) {
  event.preventDefault();

  // Get the link ID from the data attribute
  var linkId = $(linkElement).data("linkid");

  // AJAX request to add the link to the user's profile
  $.ajax({
    type: "GET",
    url: "/changecategory/" + linkId,
    success: function (response) {
      // Handle the response, e.g., show a success message
      alert(response.message);
    },
    error: function (error) {
      // Handle the error, e.g., show an error message
      console.error(error);
    },
  });
}
