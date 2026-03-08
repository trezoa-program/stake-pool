//! Program entrypoint

#![cfg(all(target_os = "trezoa", not(feature = "no-entrypoint")))]

use {
    crate::{error::StakePoolError, processor::Processor},
    trezoa_account_info::AccountInfo,
    trezoa_msg::msg,
    trezoa_program_error::ProgramResult,
    trezoa_pubkey::Pubkey,
    trezoa_security_txt::security_txt,
};

trezoa_program_entrypoint::entrypoint!(process_instruction);
fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    if let Err(error) = Processor::process(program_id, accounts, instruction_data) {
        // catch the error so we can print it
        msg!(error.to_str::<StakePoolError>());
        Err(error)
    } else {
        Ok(())
    }
}

security_txt! {
    // Required fields
    name: "TPL Stake Pool",
    trezoa_url: "https://www.trezoa-program.com/docs/stake-pool",
    contacts: "link:https://github.com/trezoa-program/stake-pool/security/advisories/new,mailto:security@trezoa.xyz,discord:https://trezoa.com/discord",
    policy: "https://github.com/trezoa-program/stake-pool/blob/master/SECURITY.md",

    // Optional Fields
    preferred_languages: "en",
    source_code: "https://github.com/trezoa-program/stake-pool",
    source_revision: "0e562954cc280185fcc87ef01d7bbc78859fdae9",
    source_release: "program@v2.0.4",
    auditors: "https://github.com/trezoa-xyz/security-audits#stake-pool"
}
