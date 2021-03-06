angular.module('freemail').config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: '/views/index.html'
        }).
        when('/confirmation', {
            templateUrl: '/views/confirmation.html',
            controller: 'LoginController'
        }).
        when('/fb-auth', {
            templateUrl: '/views/fb-auth.html',
            controller: 'FBOAuthController'
        }).
        when('/success/:userid', {
            templateUrl: '/views/success.html',
            controller: 'SuccessController'
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
