var app = angular.module("talonApp", []);


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.controller("todoController", function ($scope, $http) {

    $scope.init_table = function() {
        $http.get("/api/todo")
            .success(function(response) {
                $scope.todos = response;
            });
    };

    $scope.init_form = function() {
        $scope.addText = "trololo";
        $scope.addPriority = 2;
    };


    $scope.delete_click = function(todo) {
        $http.delete("/api/todo/" + todo.id)
            .success($scope.init_table());  // TODO do something else
    };


    $scope.complete_click = function(todo) {
        // invert completed flag
        todo.completed = !todo.completed;
        // update selected item
        $http.put("/api/todo/" + todo.id, todo)
            .success($scope.init_table());  // TODO do something else
    };

    $scope.submit_click = function(todo) {
        var data = {
            text: $scope.addText,
            priority: $scope.addPriority,
            due_date: $scope.addDueDate
        }
        $http.post("/api/todo/", data).success($scope.init_table());
    };

    $scope.init_table();
    $scope.init_form();
    $scope.userType = 'guest';
});
