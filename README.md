# Shell — Grace runtime

Shell provides Grace's ROS workspace, component links and deployment support.
Grace's receptor and persona live in [Telepathy](https://github.com/AGi-robot/telepathy).
The external WebUI lives in [Console](https://github.com/AGi-robot/console).
The parent AGi checkout supplies `AIVA/launch.sh` and runtime configuration.

## Component layout

```text
AGi/
  console/        external Telepathy Console (WebUI, outside Grace)
  AIVA/
    shell/          ROS workspace
    telepathy/      Grace entity receptor
    cypher/         shared message and codec
    health/         logging and error reporting (inside Grace)
    interactive/    conversation engine
    mind/memory/    SQLite conversation storage
```

Required links inside Shell:

```text
src/telepathy_receptor     -> ../../telepathy
src/telepathic_management  -> ../../../console
src/cryptic_signal_core    -> ../../cypher
src/agi_logging            -> ../../health
```

## Migration

Update the component dev branches together. From the AGi checkout root, if
Console is not checked out:

```sh
git clone --branch dev https://github.com/AGi-robot/console.git console
cd AIVA/shell
ln -sfn ../../../console src/telepathic_management
ln -sfn ../../telepathy src/telepathy_receptor
```

Remove stale `build/aiva_chat` and `install/aiva_chat` artifacts before building
in a fresh terminal. Install the parent AIVA requirements and source the ROS
setup configured by `paths.ros_setup` in [AIVA's spec](../spec.yaml), then run
`colcon build` inside Shell. Start Grace
with `AIVA/launch.sh`. It starts rosbridge, Health's log collector, Console and
`telepathy_receptor`, plus a model router when needed. Set `AIVA_START_CHAT=0`
to skip the receptor and local model startup. Ctrl+C shuts down managed services.

## Runtime ownership

| Component | Owner | Runtime form |
|---|---|---|
| Telepathy receptor and GraceMemory adapter | Telepathy | ROS node `/telepathy_receptor` |
| Telepathy Console | Console | Web process `telepathic_console` |
| `aiva_cryptic_signal_core` | Shell | Grace's signal scheme registry library |
| `aiva_presence` | Shell | Optional HTTP heartbeat process |
| `agi_logging` | Health | ROS node `/agi_log_collector` |
| ROS bridge and rosapi | ROS distribution | ROS nodes |
| Interactive and Memory | Their component repos | Imported Python libraries |
| llama.cpp | Model service | Separate non-ROS process |

Grace's launcher does not start AuRoRA's RAS, SCS, HRM or TMS. The retired
`aiva_chat` package has moved to Telepathy. The receptor receives encoded
`TelepathicSignal` on `/telepathic/stimulus` and emits JSON streaming events on
`/telepathic/response`. The old `/aiva/chat_input` subscription is removed.
Memory currently persists completed exchanges in SQLite and supplies eight recent
exchanges by default. Semantic retrieval is not part of this chat path.

See `AIVA/docs/telepathy-flow.md` in the parent AGi repo for the Mermaid diagram,
audit evidence and live ROS verification commands.
