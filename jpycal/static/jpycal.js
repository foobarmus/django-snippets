/* JS functions and callbacks for jpycal.
   Author: Mark Donald <mark@skagos.com.au> */

var appPrefix = '/jpycal';

function stringSub(str, arr) {
    var i, pattern, re, n = arr.length;
    for (i = 0; i < n; i++) {
        pattern = "\\{" + i + "\\}";
        re = new RegExp(pattern, "g");
        str = str.replace(re, arr[i]);
    }
    return str;
}

function lpad(thing) {
    str = thing.toString()
    return (str.length < 2) ? '0' + str : str;
}

$(document).ready(function() {

    // modal dialog controllers
    $('#allday').dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            'Create Event': function() {
                $(this).dialog('close');
                $(this).submit();
            }
        }
    });
    $('#timed').dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            'Create Event': function() {
                $(this).dialog('close');
                $(this).submit();
            }
        }
    });
    $('#allday-ed').dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            'Update Event': function() {
                $(this).dialog('close');
                $(this).submit();
            }
        }
    });
    $('#timed-ed').dialog({
        autoOpen: false,
        modal: true,
        buttons: {
            'Update Event': function() {
                $(this).dialog('close');
                $(this).submit();
            }
        }
    });

    // ajax form submission
    $('form').bind('submit', function() {
        formId = $(this).attr('id');
        if (formId.indexOf('-ed') != -1) {
            $.ajax({
                type: 'POST',
                url: appPrefix +
                     ((formId.indexOf('allday') != -1) ? $('#ad_url_ed').val() : $('#url_ed').val()),
                data: $(this).serialize(),
                success: function() {
                    $('#calendar').fullCalendar('refetchEvents');
                }
            });
        } else {
            $.ajax({
                type: 'POST',
                url: appPrefix + '/events',
                data: $(this).serialize(),
                success: function() {
                    $('#calendar').fullCalendar('refetchEvents');
                }
            });
        }
        return false;
    });

    // calendar widget
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        allDayDefault: false,
        // weekends: false, // uncomment to hide Saturdays and Sundays
        events: appPrefix + '/events',
        editable: true,
        dayClick: function(date, allDay, jsEvent, view) {
            var date_arr = [
                date.getFullYear(),
                lpad(date.getMonth() + 1), // getMonth returns 0-11
                lpad(date.getDate()),
                lpad(date.getHours()),
                lpad(date.getMinutes()),
                lpad(date.getHours() + 1)
            ];
            if (allDay) {
                $('#titledate').html(date.toDateString());
                $('#ad_start').val(stringSub('{0}-{1}-{2} 00:00', date_arr));
                $('#allday').dialog('open');
            } else {
                $('#start').val(stringSub('{0}-{1}-{2} {3}:{4}', date_arr));
                $('#end').val(stringSub('{0}-{1}-{2} {5}:{4}', date_arr));
                $('#timed').dialog('open');
            }
        },
        eventClick: function(event) {
            var date_arr = [
                event.start.getFullYear(),
                lpad(event.start.getMonth() + 1), // getMonth returns 0-11
                lpad(event.start.getDate()),
                lpad(event.start.getHours()),
                lpad(event.start.getMinutes())
            ];
            if (event.allDay == true) {
                $('#ad_title_ed').val(event.title);
                $('#ad_description_ed').val(event.description);
                $('#titledate_ed').html(event.start.toDateString());
                $('#ad_start_ed').val(stringSub('{0}-{1}-{2} 00:00', date_arr));
                $('#ad_url_ed').val(event.url);
                $('#allday-ed').dialog('open');
            } else {
                date_arr.push(event.end.getHours());
                $('#title_ed').val(event.title);
                $('#start_ed').val(stringSub('{0}-{1}-{2} {3}:{4}', date_arr));
                $('#end_ed').val(stringSub('{0}-{1}-{2} {5}:{4}', date_arr));
                $('#description_ed').val(event.description);
                $('#url_ed').val(event.url);
                $('#timed-ed').dialog('open');
            }
            return false;
        },
        eventDrop: function(event, dayDelta, minuteDelta, allDay) {
            var start = [
                event.start.getFullYear(),
                lpad(event.start.getMonth() + 1),
                lpad(event.start.getDate()),
                lpad(event.start.getHours()),
                lpad(event.start.getMinutes())
            ];
            var end = (event.end) ? [
                event.end.getFullYear(),
                lpad(event.end.getMonth() + 1),
                lpad(event.end.getDate()),
                lpad(event.end.getHours()),
                lpad(event.end.getMinutes())
            ] : start;
            
            $.ajax({
                type: 'PUT',
                url: appPrefix + event.url,
                data: {
                    start: stringSub('{0}-{1}-{2} {3}:{4}', start),
                    end: stringSub('{0}-{1}-{2} {3}:{4}', end),
                    allDay: allDay
                }
            });
        },
        eventResize: function(event) {
            var end = [
                event.end.getFullYear(),
                lpad(event.end.getMonth() + 1),
                lpad(event.end.getDate()),
                lpad(event.end.getHours()),
                lpad(event.end.getMinutes())
            ];
            $.ajax({
                type: 'PUT',
                url: appPrefix + event.url,
                data: {end: stringSub('{0}-{1}-{2} {3}:{4}', end)}
            });
        }
    });

});
