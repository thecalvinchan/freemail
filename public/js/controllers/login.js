angular.module('freemail').controller('LoginController', ['$scope','$http','$cookieStore','$location',
    function ($scope,$http,$cookieStore,$location) {
        $scope.email;
        $scope.password;
        $scope.submit = function() {
            var data = {
                email: $scope.email,
                password: $scope.password
            };
            console.log(data);
            var config = {
                method : 'POST',
                url : '/login',
                data : JSON.stringify(data),
                xsrfHeaderName : 'X-CSRFToken',
                xsrfCookieName : 'csrftoken'
            };
            $http(config).success(function(data) {
                console.log(data);
                $cookieStore.put('user_id',data.user_id);
                $cookieStore.put('session',data.session);
                $location.path('/fb-auth');
            }).error(function(err) {
                document.getElementById('email-textarea').innerHTML=err;
            });
        }
    }
]);

angular.module('freemail').controller('FBOAuthController', ['$scope','$http','$cookieStore','$location',
    function ($scope,$http,$cookieStore,$location) {
        $scope.auth = function() {
            FB.login(function(response) {
                if (response.authResponse) {
                    FB.api('/me?username', function(response) {
                        var data = {
                            user_id : $cookieStore.get('user_id'),
                            session : $cookieStore.get('session'),
                            fbemail : response.username+'@facebook.com'
                        };
                        console.log(data);
                        var config = {
                            method : 'POST',
                            url : '/user',
                            data : JSON.stringify(data),
                            xsrfHeaderName : 'X-CSRFToken',
                            xsrfCookieName : 'csrftoken'
                        };
                        $http(config).success(function(data) {
                            $location.path('/success');
                        }).error(function(err) {
                            console.log(err);
                            document.getElementById('email-textarea').innerHTML=err;
                        });
                    });
                } else {
                    //User cancelled login
                }
            });
        };
    }
]);
