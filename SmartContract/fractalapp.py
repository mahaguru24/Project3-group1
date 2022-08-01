import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
# from ethereum import w3, generate_account, get_balance, send_transaction

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/fractaltoken_abi.json')) as f:
        artwork_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


st.title("Fractal Registration")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")


################################################################################
# Register New Artwork
################################################################################
st.markdown("## Register New Fractal")
artwork_name = st.text_input("Enter the name of Fractal")
initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
if st.button("Register Fractal"):
    artwork_ipfs_hash = pin_artwork(artwork_name, file)
    artwork_uri = f"ipfs://{artwork_ipfs_hash}"
    tx_hash = contract.functions.registerArtwork(
        address,
        artwork_name,
        int(initial_appraisal_value),
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")

################################################################################
# Appraise Art
################################################################################
st.markdown("## Purchase Fractal")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose a Fractal ID", list(range(tokens)))
new_appraisal_value = st.text_input("Buy price")
appraisal_report_content = st.text_area("Extra details")
if st.button("Buy Fractal"):

    # Use Pinata to pin an appraisal report for the report URI
    appraisal_report_ipfs_hash =  pin_appraisal_report(appraisal_report_content)
    report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

    # Use the token_id and the report_uri to record the appraisal
    tx_hash = contract.functions.newAppraisal(
        token_id,
        int(new_appraisal_value),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt1 = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt1)
st.markdown("---")

################################################################################
# Get Transaction Information
################################################################################
st.markdown("## Get the appraisal report history")
art_token_id = st.number_input("Fractal ID", value=0, step=1)
if st.button("Get Appraisal Reports"):
    appraisal_filter = contract.events.Appraisal.createFilter(
        fromBlock=0, argument_filters={"tokenId": art_token_id}
    )
    reports = appraisal_filter.get_all_entries()
    if reports:
        for report in reports:
            report_dictionary = dict(report)
            st.markdown("### Appraisal Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Appraisal Event Details")
            st.write(report_dictionary["args"])
    else:
        st.write("Fractal has no new appraisals")