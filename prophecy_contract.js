// Smart contract for storing prophecies on NEAR
export function init() {
  // Initialize an empty storage
}

// Store a prophecy
export function set_prophecy({ prophecy_id, prophecy_data }) {
  // Verify that the caller is the contract owner
  assert(
    context.predecessor === context.contractName,
    "Only the contract owner can store prophecies"
  );
  
  // Store the prophecy
  storage.set(prophecy_id, prophecy_data);
  return true;
}

// Retrieve a prophecy
export function get_prophecy({ prophecy_id }) {
  return storage.get(prophecy_id);
}
