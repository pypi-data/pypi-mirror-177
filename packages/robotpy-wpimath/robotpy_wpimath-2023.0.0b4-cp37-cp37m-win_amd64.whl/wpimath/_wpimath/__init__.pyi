from __future__ import annotations
import wpimath._wpimath
import typing
import wpimath.geometry._geometry

__all__ = [
    "angleModulus",
    "applyDeadband",
    "calculateDistanceToTarget",
    "estimateCameraToTarget",
    "estimateFieldToCamera",
    "estimateFieldToRobot",
    "inputModulus"
]


def angleModulus(angle: radians) -> radians:
    pass
def applyDeadband(value: float, deadband: float, maxMagnitude: float = 1.0) -> float:
    """
    Returns 0.0 if the given value is within the specified range around zero. The
    remaining range between the deadband and the maximum magnitude is scaled from
    0.0 to the maximum magnitude.

    :param value:        Value to clip.
    :param deadband:     Range around zero.
    :param maxMagnitude: The maximum magnitude of the input (defaults to 1). Can
                         be infinite.

    :returns: The value after the deadband is applied.
    """
def calculateDistanceToTarget(cameraHeight: meters, targetHeight: meters, cameraPitch: radians, targetPitch: radians, targetYaw: radians) -> meters:
    pass
def estimateCameraToTarget(cameraToTargetTranslation: wpimath.geometry._geometry.Translation3d, fieldToTarget: wpimath.geometry._geometry.Pose3d, gyroAngle: wpimath.geometry._geometry.Rotation2d) -> wpimath.geometry._geometry.Transform3d:
    pass
def estimateFieldToCamera(cameraToTarget: wpimath.geometry._geometry.Transform3d, fieldToTarget: wpimath.geometry._geometry.Pose3d) -> wpimath.geometry._geometry.Pose3d:
    pass
@typing.overload
def estimateFieldToRobot(cameraHeight: meters, targetHeight: meters, cameraPitch: radians, targetPitch: radians, targetYaw: wpimath.geometry._geometry.Rotation2d, gyroAngle: wpimath.geometry._geometry.Rotation2d, fieldToTarget: wpimath.geometry._geometry.Pose3d, cameraToRobot: wpimath.geometry._geometry.Transform3d) -> wpimath.geometry._geometry.Pose3d:
    pass
@typing.overload
def estimateFieldToRobot(cameraToTarget: wpimath.geometry._geometry.Transform3d, fieldToTarget: wpimath.geometry._geometry.Pose3d, cameraToRobot: wpimath.geometry._geometry.Transform3d) -> wpimath.geometry._geometry.Pose3d:
    pass
def inputModulus(input: float, minimumInput: float, maximumInput: float) -> float:
    """
    Returns modulus of input.

    :param input:        Input value to wrap.
    :param minimumInput: The minimum value expected from the input.
    :param maximumInput: The maximum value expected from the input.
    """
