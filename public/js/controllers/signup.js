angular.module('freemail').controller('SignupController', ['$scope','$http','$cookies',
    function ($scope,$http,$cookies) {
	$http
	console.log($cookies.csrftoken);
        $scope.email;
        $scope.password;
        $scope.confirmpassword;
        $scope.submit = function() {
            if ($scope.confirmpassword != $scope.password) {
                $scope.error = "Your passwords do not match.";
                return;
            }
            var data = {
                email: $scope.email,
                password: $scope.password
            };
            console.log(data);
            var config = {
                method : 'POST',
                url : '/confirmation',
                data : JSON.stringify(data),
                xsrfHeaderName : 'X-CSRFToken',
                xsrfCookieName : 'csrftoken'
            };
            $http(config).success(function(data) {
                var modal = document.getElementById('signupModal');
                modal.innerHTML = '\
                    <h4 class="text-center">Awesome! Confirmation Email Sent.</h4>\
                    <hr>\
                    <p class="text-center">Please check your email for further instructions.</p>\
                    <a class="close-reveal-modal">&#215;</a>\
                ';
		console.log(data);
            }).error(function(err) {
                var modal = document.getElementById('signupModal');
                modal.innerHTML = '\
                    <h4 class="text-center">Oops! Something went wrong.</h4>\
                    <hr>\
                    <p class="text-center">' + err + '.</p>\
                    <a class="close-reveal-modal">&#215;</a>\
                ';
            });
        }
    }
]);
