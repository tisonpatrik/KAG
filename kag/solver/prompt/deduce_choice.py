import logging
from typing import List

from kag.interface import PromptABC

logger = logging.getLogger(__name__)


@PromptABC.register("default_deduce_choice")
class DeduceChoice(PromptABC):
    template_zh = (
        "根据提供的选项及相关答案，请选择其中一个选项回答问题“$instruction”。"
        "无需解释；"
        "如果没有可选择的选项，直接回复“无相关信息”无需解释"
        "注意，只能根据输入的信息进行推断，不允许进行任何假设"
        "\n【信息】：“$memory”\n请确保所提供的信息直接准确地来自检索文档，不允许任何自身推测。"
    )
    template_en = (
        "Based on the provided options and related answers, choose one option to respond to the question '$instruction'."
        "No explanation is needed;"
        "If there are no available options, simply reply 'No relevant information' without explanation."
        "\n[Information]: '$memory'"
        "\nEnsure that the information provided comes directly and accurately from the retrieved document, "
        "without any speculation."
    )

    @property
    def template_variables(self) -> List[str]:
        return ["memory", "instruction"]

    def parse_response_en(self, satisfied_info: str):
        if satisfied_info.startswith("No relevant information"):
            if_answered = False
        else:
            if_answered = True
        return if_answered, satisfied_info

    def parse_response_zh(self, satisfied_info: str):
        if satisfied_info.startswith("无相关信息"):
            if_answered = False
        else:
            if_answered = True
        return if_answered, satisfied_info

    def parse_response(self, response: str, **kwargs):
        logger.debug("推理器判别:{}".format(response))
        if self.language == "en":
            return self.parse_response_en(response)
        return self.parse_response_zh(response)
