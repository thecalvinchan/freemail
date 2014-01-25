angular.module('freemail').config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: '/views/index.html'
        }).
        when('/confirmation-sent', {
            templateUrl: '/views/confirmation-sent.html'
        }).
        otherwise({
            redirectTo: '/'
        });
    }
]);

angular.module('freemail').config(['$locationProvider',
    function($locationProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix("!");
    }
]);
