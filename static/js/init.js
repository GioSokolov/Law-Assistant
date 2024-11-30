$(document).ready(function() {
    $(".countdown").countdown({
        date: "16 April 1879 00:04:00",
        format: "on"
    },
    function() {
        // callback function
        console.log("Countdown completed!");
    });
});
