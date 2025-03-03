import { storage, Context, assert } from "near-sdk-as";

// Initialize storage
export function init(): void {
  // No initialization needed for simple key-value storage
}

// Store a prophecy
export function set_prophecy(prophecy_id: string, prophecy_data: string): boolean {
  // Only contract owner can store prophecies
  assert(Context.sender == Context.contractName, "Only contract owner can store prophecies");

  storage.set(prophecy_id, prophecy_data);
  return true;
}

// Retrieve a prophecy
export function get_prophecy(prophecy_id: string): string | null {
  return storage.get<string>(prophecy_id);
}