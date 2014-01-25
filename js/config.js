angular.module('freemail').config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: '/views/index.html'
        });
    }
]);
