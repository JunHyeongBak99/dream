# AI 기반 꿈 해몽 시스템

최신 AI 기술을 활용해 꿈을 자동으로 분석하고 개인 맞춤형 해석을 제공하는 혁신적인 서비스입니다. 이 프로젝트는 정신적 웰빙을 지원하고, 자아 탐색의 도구로서 꿈의 의미를 효율적으로 분석하는 것을 목표로 합니다.

## 프로젝트 소개
현대 사회에서 정신적 웰빙과 자아 탐색의 중요성이 커짐에 따라, 많은 사람들이 꿈의 의미를 이해하고자 합니다. 그러나 기존의 유료 해몽 서비스는 경제적 부담과 비효율적인 사용 경험을 제공합니다. 이에 따라, 본 프로젝트는 KoBERT와 GPT 모델을 활용하여 사용자 개별 상황에 맞춘 개인화된 해석을 제공하고, 자동화된 해몽 서비스를 통해 사용자가 쉽게 꿈의 의미를 분석할 수 있도록 합니다.

- **개인 맞춤형 해석**: 단순한 패턴 매칭이 아닌, 사용자의 상황에 맞춘 해몽 결과 제공.
- **경제적 부담 감소**: 자동화된 AI 서비스로 효율적이고 경제적인 해몽 지원.
- **한국어 최적화**: 한국어 자연어 처리 강화를 통해 최적화된 사용자 경험 제공.
- **지속적 데이터 분석**: 꿈 데이터를 저장 및 분석하여 반복적인 경향을 파악하고, 심리 상태와 자아 탐색 지원.

## 시스템 구조
### Frontend
- **웹/모바일 UI**: 사용자 친화적인 인터페이스를 통해 꿈 데이터를 입력하고 해몽 결과를 확인할 수 있습니다.

### Backend
- **KoBERT**: 한국어 자연어 처리를 위한 KoBERT 모델을 사용해 꿈 데이터를 분석합니다.
- **GPT**: 꿈의 복잡한 의미를 해석하기 위한 자연어 처리 모델.
- **RAG (Retrieval-Augmented Generation)**: 꿈과 관련된 실시간 정보 검색을 통해 더욱 풍부한 해몽 결과 제공.

### 데이터 처리 및 저장
- **데이터베이스**: 꿈 데이터를 저장하고 지속적으로 분석하여 개인화된 서비스 제공.
- **반복적인 패턴 분석**: 사용자의 꿈 기록을 분석해 반복되는 꿈 경향을 파악하고 이를 바탕으로 심리 상태를 해석.

## 개발 일정

| 주차       | 주요 활동              | 목표 및 기능                                               |
|------------|------------------------|------------------------------------------------------------|
| 1-4주차    | 계획 수립 및 기획서 작성  | **4주차**: 계획서 발표                                      |
| 5-8주차    | 1st 프로토타입 개발     | **목표**: 꿈 입력 및 해석 기능, KoBERT 모델 연동, 간단한 UI 제공<br> **8주차**: 중간평가 |
| 9-12주차   | 2nd 프로토타입 개발     | **목표**: RAG 기반 검색 및 GPT 기반 해석 결과 제공, 데이터 저장 및 관리 기능<br> **12주차**: 중간점검 |
| 13-15주차  | 최종 기능 개발 및 통합  | **목표**: 전체 기능 통합, 사용자 맞춤형 해몽 제공, 최적화된 UI/UX<br> **15주차**: 최종 발표 |


## 프로젝트 목표
이 AI 기반 꿈 해몽 시스템은 정신적 웰빙을 개선하고, 사용자 맞춤형 해몽 서비스를 통해 더욱 의미 있는 경험을 제공합니다. 꿈 데이터를 기반으로 자아 탐색을 지원하며, 꿈의 반복적인 패턴을 분석하여 사용자의 심리 상태 파악을 돕습니다.
