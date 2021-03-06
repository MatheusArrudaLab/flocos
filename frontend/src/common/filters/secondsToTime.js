/**
  * Filter for converting second to HH:mm:ss time
  * @ngInject
  */

angular.module('flocs.filters')
.filter('secondsToTime', function($filter) {
    return function(seconds) {
        var format = (seconds >= 3600) ? 'H:mm:ss' : "m:ss";
        return $filter('date')(new Date(0, 0, 0).setSeconds(seconds), format);
    };
});
