use cf_core_alpha::session;
use pyo3::prelude::*;
use std::thread;
use tokio::runtime::Runtime;

fn capabilities() -> anyhow::Result<session::Capabilities> {
    Ok(session::Capabilities {
        shell: true,
        actions: None,
    })
}

/// Background loop to read incoming messages from the Relay service.
async fn async_loop() {
    let agent = cf_core_alpha::Agent::from_env(capabilities).unwrap();
    agent.run().await;
}

/// entrypoint to the Python module. This is where Python methods are registered.
#[pymodule]
pub fn commonfate_access(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    // // register the action function in our module
    // module.add_function(wrap_pyfunction!(action, module)?)?;

    // when imported, spin up a background thread to connect to the Relay
    thread::spawn(move || {
        let rt = Runtime::new().unwrap();
        rt.block_on(async_loop());
    });

    Ok(())
}
