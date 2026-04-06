"""
Script para processar arquivos NF-e XML da pasta data/origem,
adicionar protocolo de autorização e salvar formatados em data/destino.

Uso: python process_nfe.py
"""

import re
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom

ORIGEM = Path(__file__).parent / "data" / "origem"
DESTINO = Path(__file__).parent / "data" / "destino"

NS = "http://www.portalfiscal.inf.br/nfe"
NS_SIG = "http://www.w3.org/2000/09/xmldsig#"

ET.register_namespace("", NS)
ET.register_namespace("ds", NS_SIG)


def extrair_chave(xml_path: Path) -> str:
    """Extrai a chave de acesso (44 dígitos) do nome do arquivo."""
    nome = xml_path.stem
    return nome.replace("NFe", "")


def get_text(root, tag_local) -> str:
    el = root.find(f".//{{{NS}}}{tag_local}")
    return el.text.strip() if el is not None and el.text else ""


def get_digest_value(root) -> str:
    el = root.find(f".//{{{NS_SIG}}}DigestValue")
    return el.text.strip() if el is not None and el.text else ""


def formatar_nfe(nfe_el: ET.Element) -> str:
    """Serializa o elemento NFe formatado, removendo CDATA do qrCode."""
    raw = ET.tostring(nfe_el, encoding="unicode")
    # Remove CDATA mantendo conteúdo limpo
    raw = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", raw, flags=re.DOTALL)
    dom = minidom.parseString(raw.encode("utf-8"))
    pretty = dom.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
    # Remove a declaração XML (será adicionada manualmente)
    lines = pretty.splitlines()
    if lines and lines[0].startswith("<?xml"):
        lines = lines[1:]
    # Indentar bloco inteiro com 2 espaços (ficará dentro de <nfeProc>)
    indented = "\n".join("  " + line if line.strip() else "" for line in lines)
    return indented.rstrip()


def bloco_prot_nfe(chave: str, tp_amb: str, dh_emi: str, nProt: str, dig_val: str) -> str:
    """Gera o bloco <protNFe> com a indentação padrão do sistema."""
    return (
        f'  <protNFe versao="4.00">\n'
        f"          <infProt>\n"
        f"            <tpAmb>{tp_amb}</tpAmb>\n"
        f"            <verAplic>SVRSnfce2512111137DR</verAplic>\n"
        f"            <chNFe>{chave}</chNFe>\n"
        f"            <dhRecbto>{dh_emi}</dhRecbto>\n"
        f"            <nProt>{nProt}</nProt>\n"
        f"            <digVal>{dig_val}</digVal>\n"
        f"            <cStat>100</cStat>\n"
        f"            <xMotivo>Autorizado o uso da NF-e</xMotivo>\n"
        f"          </infProt>\n"
        f"        </protNFe>"
    )


def processar_arquivo(xml_path: Path, nProt: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Suporte a arquivos que já estejam em nfeProc
    if root.tag == f"{{{NS}}}nfeProc":
        nfe_el = root.find(f"{{{NS}}}NFe")
    else:
        nfe_el = root

    chave = extrair_chave(xml_path)
    tp_amb = get_text(nfe_el, "tpAmb") or "1"
    dh_emi = get_text(nfe_el, "dhEmi")
    dig_val = get_digest_value(nfe_el)

    nfe_formatado = formatar_nfe(nfe_el)
    prot_block = bloco_prot_nfe(chave, tp_amb, dh_emi, nProt, dig_val)

    xml_final = (
        "<?xml version='1.0' encoding='utf-8'?>\n"
        f'<nfeProc versao="4.00" xmlns="{NS}">\n'
        f"{nfe_formatado}\n"
        f"{prot_block}\n"
        "</nfeProc>\n"
    )

    nome_saida = f"NFe{chave}-nfe.xml"
    destino_path = DESTINO / nome_saida
    destino_path.write_text(xml_final, encoding="utf-8")
    print(f"  Salvo: {destino_path.name}")


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)

    arquivos = sorted(ORIGEM.glob("*.xml"))
    if not arquivos:
        print("Nenhum arquivo XML encontrado em data/origem.")
        return

    print(f"Encontrados {len(arquivos)} arquivo(s) em data/origem.\n")

    for xml_path in arquivos:
        print(f"Chave: {extrair_chave(xml_path)}")
        nProt = input("  Protocolo de autorização: ").strip()
        if not nProt:
            print("  Protocolo em branco, pulando.\n")
            continue
        try:
            processar_arquivo(xml_path, nProt)
        except Exception as e:
            print(f"  ERRO: {e}")
        print()

    print("Processamento concluído.")


if __name__ == "__main__":
    main()
