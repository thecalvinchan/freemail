angular.module('freemail').controller('SignupController', ['$scope','$location',
    function ($scope,$location) {
        $scope.email;
        $scope.submit = function() {
            console.log($scope.email);
            $location.path('confirmation-sent');
        }
    }
]);
