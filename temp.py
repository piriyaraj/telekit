
    $(
        document).ready(function () {

        var total_record = 0;

        var total_groups = 85199;
        $('#results').load("https://groupsorlink.com/telegram/group/loadresult", {'group_no': total_record,'home' : true}, function () {
           total_record = total_record + 1;
        });
        $(document).on('click', '#load_more', function () {
            $("#load_more").hide();
            if (total_record <= total_groups)
            {
                loading = true;
                    $("#report").show();
                    $.post('https://groupsorlink.com/telegram/group/loadresult', {'group_no': total_record,'home' : true},
                        function (data) {
                            if (data !== "") {
                                $("#results").append(data);
                                $("#report").hide();
                                $("#load_more").show();
                                total_record++;
                            } else {
                                $("#report").hide();
                                $("#no").show();
                                $("#load_more").hide();
                            }
                        });
            }


        });
    });
