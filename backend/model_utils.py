from typing import Optional, Tuple
from google.genai import types

def prepare_model_and_config(
    modelo_solicitado: Optional[str] = "padrao",
    default_model: str = "gemini-2.5-flash",
    default_temp: Optional[float] = 0.4,
    response_mime_type: Optional[str] = None,
    response_schema: Optional[type] = None,
    tools: Optional[list] = None,
    system_instruction: Optional[str] = None
) -> Tuple[str, types.GenerateContentConfig]:
    """
    Retorna o nome do modelo e a estrutura GenerateContentConfig.
    Se o modelo solicitado for 'gemini-3.5-flash-lite', substitui o modelo
    e OMITE ESTRITAMENTE o parâmetro 'temperature'.
    """
    is_flash_lite = bool(modelo_solicitado and "3.5-flash-lite" in str(modelo_solicitado).lower())
    
    selected_model = "gemini-3.5-flash-lite" if is_flash_lite else default_model

    kwargs = {}
    # ESTRITAMENTE OMITIR TEMPERATURE SE FOR GEMINI 3.5 FLASH-LITE
    if not is_flash_lite and default_temp is not None:
        kwargs["temperature"] = default_temp

    if response_mime_type:
        kwargs["response_mime_type"] = response_mime_type
    if response_schema:
        kwargs["response_schema"] = response_schema
    if tools:
        kwargs["tools"] = tools
    if system_instruction:
        kwargs["system_instruction"] = system_instruction

    config = types.GenerateContentConfig(**kwargs)
    return selected_model, config
