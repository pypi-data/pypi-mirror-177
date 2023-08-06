// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc2/command/button/Trigger.h"

#include <frc/filter/Debouncer.h>

#include "frc2/command/InstantCommand.h"

using namespace frc;
using namespace frc2;

Trigger::Trigger(const Trigger& other) = default;

Trigger Trigger::OnTrue(std::shared_ptr<Command> command) {
  m_event.Rising().IfHigh([command] { Command_Schedule(command); });
  return *this;
}

/*
Trigger Trigger::OnTrue(CommandPtr&& command) {
  m_event.Rising().IfHigh(
      [command = std::move(command)] { command.Schedule(); });
  return *this;
}
*/

Trigger Trigger::OnFalse(std::shared_ptr<Command> command) {
  m_event.Falling().IfHigh([command] { Command_Schedule(command); });
  return *this;
}

/*
Trigger Trigger::OnFalse(CommandPtr&& command) {
  m_event.Falling().IfHigh(
      [command = std::move(command)] { command.Schedule(); });
  return *this;
}
*/

Trigger Trigger::WhileTrue(std::shared_ptr<Command> command) {
  m_event.Rising().IfHigh([command] { Command_Schedule(command); });
  m_event.Falling().IfHigh([command] { command->Cancel(); });
  return *this;
}

/*
Trigger Trigger::WhileTrue(CommandPtr&& command) {
  auto ptr = std::make_shared<CommandPtr>(std::move(command));
  m_event.Rising().IfHigh([ptr] { ptr->Schedule(); });
  m_event.Falling().IfHigh([ptr] { ptr->Cancel(); });
  return *this;
}
*/

Trigger Trigger::WhileFalse(std::shared_ptr<Command> command) {
  m_event.Falling().IfHigh([command] { Command_Schedule(command); });
  m_event.Rising().IfHigh([command] { command->Cancel(); });
  return *this;
}

/*
Trigger Trigger::WhileFalse(CommandPtr&& command) {
  auto ptr = std::make_shared<CommandPtr>(std::move(command));
  m_event.Falling().IfHigh([ptr] { ptr->Schedule(); });
  m_event.Rising().IfHigh([ptr] { ptr->Cancel(); });
  return *this;
}
*/

Trigger Trigger::ToggleOnTrue(std::shared_ptr<Command> command) {
  m_event.Rising().IfHigh([command] {
    if (command->IsScheduled()) {
      command->Cancel();
    } else {
      Command_Schedule(command);
    }
  });
  return *this;
}

/*
Trigger Trigger::ToggleOnTrue(CommandPtr&& command) {
  m_event.Rising().IfHigh([command = std::move(command)] {
    if (command.IsScheduled()) {
      command.Cancel();
    } else {
      command.Schedule();
    }
  });
  return *this;
}
*/

Trigger Trigger::ToggleOnFalse(std::shared_ptr<Command> command) {
  m_event.Falling().IfHigh([command] {
    if (command->IsScheduled()) {
      command->Cancel();
    } else {
      Command_Schedule(command);
    }
  });
  return *this;
}

/*
Trigger Trigger::ToggleOnFalse(CommandPtr&& command) {
  m_event.Falling().IfHigh([command = std::move(command)] {
    if (command.IsScheduled()) {
      command.Cancel();
    } else {
      command.Schedule();
    }
  });
  return *this;
}
*/

WPI_IGNORE_DEPRECATED
Trigger Trigger::WhenActive(std::shared_ptr<Command> command) {
  m_event.Rising().IfHigh([command] { Command_Schedule(command); });
  return *this;
}

// Trigger Trigger::WhenActive(std::function<void()> toRun,
//                             std::initializer_list<std::shared_ptr<Subsystem>> requirements) {
//   return WhenActive(std::move(toRun),
//                     {requirements.begin(), requirements.end()});
// }

Trigger Trigger::WhenActive(std::function<void()> toRun,
                            std::span<std::shared_ptr<Subsystem>> requirements) {
  return WhenActive(InstantCommand(std::move(toRun), requirements));
}

Trigger Trigger::WhileActiveContinous(std::shared_ptr<Command> command) {
  m_event.IfHigh([command] { Command_Schedule(command); });
  m_event.Falling().IfHigh([command] { command->Cancel(); });
  return *this;
}

// Trigger Trigger::WhileActiveContinous(
//     std::function<void()> toRun,
//     std::initializer_list<std::shared_ptr<Subsystem>> requirements) {
//   return WhileActiveContinous(std::move(toRun),
//                               {requirements.begin(), requirements.end()});
// }

Trigger Trigger::WhileActiveContinous(
    std::function<void()> toRun, std::span<std::shared_ptr<Subsystem>> requirements) {
  return WhileActiveContinous(InstantCommand(std::move(toRun), requirements));
}

Trigger Trigger::WhileActiveOnce(std::shared_ptr<Command> command) {
  m_event.Rising().IfHigh([command] { Command_Schedule(command); });
  m_event.Falling().IfHigh([command] { command->Cancel(); });
  return *this;
}

Trigger Trigger::WhenInactive(std::shared_ptr<Command> command) {
  m_event.Falling().IfHigh([command] { Command_Schedule(command); });
  return *this;
}

// Trigger Trigger::WhenInactive(std::function<void()> toRun,
//                               std::initializer_list<std::shared_ptr<Subsystem>> requirements) {
//   return WhenInactive(std::move(toRun),
//                       {requirements.begin(), requirements.end()});
// }

Trigger Trigger::WhenInactive(std::function<void()> toRun,
                              std::span<std::shared_ptr<Subsystem>> requirements) {
  return WhenInactive(InstantCommand(std::move(toRun), requirements));
}

Trigger Trigger::ToggleWhenActive(std::shared_ptr<Command> command) {
  m_event.Rising().IfHigh([command] {
    if (command->IsScheduled()) {
      command->Cancel();
    } else {
      Command_Schedule(command);
    }
  });
  return *this;
}

Trigger Trigger::CancelWhenActive(std::shared_ptr<Command> command) {
  m_event.Rising().IfHigh([command] { command->Cancel(); });
  return *this;
}
WPI_UNIGNORE_DEPRECATED

BooleanEvent Trigger::GetEvent() const {
  return m_event;
}
