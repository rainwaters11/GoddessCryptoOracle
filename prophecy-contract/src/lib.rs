use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::serde::{Deserialize, Serialize};
use near_sdk::{env, near_bindgen, AccountId, PanicOnDefault};
use near_sdk::collections::UnorderedMap;

#[derive(BorshDeserialize, BorshSerialize, Serialize, Deserialize)]
#[serde(crate = "near_sdk::serde")]
pub struct Prophecy {
    pub text: String,
    pub timestamp: u64,
    pub creator: AccountId,
}

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize, PanicOnDefault)]
pub struct ProphecyOracle {
    prophecies: UnorderedMap<String, Prophecy>,
    owner_id: AccountId,
}

#[near_bindgen]
impl ProphecyOracle {
    #[init]
    pub fn new(owner_id: AccountId) -> Self {
        Self {
            prophecies: UnorderedMap::new(b"p"),
            owner_id,
        }
    }

    pub fn store_prophecy(&mut self, prophecy_id: String, text: String) {
        assert_eq!(
            env::predecessor_account_id(),
            self.owner_id,
            "Only the owner can store prophecies"
        );

        let prophecy = Prophecy {
            text,
            timestamp: env::block_timestamp(),
            creator: env::predecessor_account_id(),
        };

        self.prophecies.insert(&prophecy_id, &prophecy);
        env::log_str(&format!("Stored prophecy: {}", prophecy_id));
    }

    pub fn get_prophecy(&self, prophecy_id: String) -> Option<Prophecy> {
        self.prophecies.get(&prophecy_id)
    }

    pub fn get_latest_prophecies(&self, limit: u64) -> Vec<(String, Prophecy)> {
        self.prophecies
            .iter()
            .take(limit as usize)
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use near_sdk::test_utils::VMContextBuilder;
    use near_sdk::testing_env;

    fn get_context(predecessor: AccountId) -> VMContextBuilder {
        let mut builder = VMContextBuilder::new();
        builder.predecessor_account_id(predecessor);
        builder
    }

    #[test]
    fn test_store_and_get_prophecy() {
        let owner: AccountId = "oracle.near".parse().unwrap();
        let context = get_context(owner.clone());
        testing_env!(context.build());

        let mut contract = ProphecyOracle::new(owner);
        let prophecy_id = "test_prophecy".to_string();
        let prophecy_text = "The future of Web3 is bright!".to_string();

        contract.store_prophecy(prophecy_id.clone(), prophecy_text.clone());

        let stored_prophecy = contract.get_prophecy(prophecy_id).unwrap();
        assert_eq!(stored_prophecy.text, prophecy_text);
    }
}