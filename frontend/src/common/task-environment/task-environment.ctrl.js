/*
 * Task Environment controller
 */
angular.module('flocs.taskEnvironment')
.controller('taskEnvironmentCtrl', ['$scope', 'taskEnvironmentService', 'interpreterService',
  function($scope, taskEnvironmentService, interpreterService) {

  function run() {
    //$scope.initialState = false;
    taskEnvironmentService.runningCode();
    /*.then(function(result) {
      if (result.solved) {
        $scope.initialState = true;
      }
    });*/
  }

  function reset() {
    taskEnvironmentService.stoppingExecution();
    /*.then(function(result) {
      $scope.initialState = true;
    });*/
  }

  /*function handleTaskEnvironmentChange() {
    $scope.blocksStatus.used = taskEnvironmentService.getBlocksUsed();
    $scope.blocksStatus.limit = taskEnvironmentService.getBlocksLimit();
  }*/

  $scope.changeSpeedClicked = function() {
    interpreterService.setSpeed($scope.settings.speed);
  };

  $scope.availableSpeeds = interpreterService.getAvailableSpeeds();
  $scope.settings = {
    speed: interpreterService.getSpeed()
  };

  $scope.executionStatus = taskEnvironmentService.executionStatus;
  $scope.blocksStatus = taskEnvironmentService.blocksStatus;
  $scope.toolsStatus = taskEnvironmentService.toolsStatus;
  $scope.instructions = taskEnvironmentService.instructions;
  $scope.run = run;
  $scope.reset = reset;

}]);
