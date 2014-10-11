var app = angular.module("talonApp", []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.controller("todoController", function ($scope, $http) {

    $scope.init = function() {
        $http.get("/api/todo")
            .success(function(response) {
                $scope.todos = response;
            });
    };

    $scope.delete_click = function(todo) {
        $http.delete("/api/todo/" + todo.id)
            .success(function(response) {
                $scope.init(); // TODO do something else
            });

    };

    $scope.complete_click = function(todo) {

        todo.completed = !todo.completed

        $http.put("/api/todo/" + todo.id, todo)
            .success(function(response) {
                $scope.init(); // TODO do something else
            });
    };

    $scope.init();

});